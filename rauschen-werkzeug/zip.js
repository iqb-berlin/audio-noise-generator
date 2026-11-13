// Minimal ZIP writer for "Alle speichern". Stores the files without compression: audio and video are
// compressed already, deflating them again would only cost time. Format: PKWARE APPNOTE.TXT, section 4.3.
// Limits: no ZIP64, so each file and the whole archive must stay below 4 GB and below 65535 entries.

const CRC_TABLE = new Uint32Array(256).map((_, n) => {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});

function crc32(bytes) {
  let c = 0xFFFFFFFF;
  for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}

// Little-endian record from [byteCount, value] pairs
function record(fields) {
  const view = new DataView(new ArrayBuffer(fields.reduce((n, [size]) => n + size, 0)));
  let pos = 0;
  for (const [size, value] of fields) {
    if (size === 2) view.setUint16(pos, value, true); else view.setUint32(pos, value, true);
    pos += size;
  }
  return new Uint8Array(view.buffer);
}

function dosDateTime(d) {
  return {
    time: (d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1),
    date: ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate(),
  };
}

// files: [{ name, blob }] -> Blob of a ZIP archive. Names are stored as UTF-8 (general purpose flag bit 11).
export async function zipStore(files, now = new Date()) {
  const UTF8 = 0x0800, VERSION = 20, MAX = 0xFFFFFFFF;
  if (files.length >= 0xFFFF) throw new Error('Zu viele Dateien für eine ZIP-Datei');
  const { time, date } = dosDateTime(now);
  const encoder = new TextEncoder(), local = [], central = [];
  let offset = 0;
  for (const { name, blob } of files) {
    const data = new Uint8Array(await blob.arrayBuffer());
    const nameBytes = encoder.encode(name), crc = crc32(data), size = data.length;
    if (size >= MAX || offset + 30 + nameBytes.length + size >= MAX) throw new Error('ZIP-Datei würde größer als 4 GB');
    const common = [[2, VERSION], [2, UTF8], [2, 0], [2, time], [2, date], [4, crc], [4, size], [4, size], [2, nameBytes.length], [2, 0]];
    local.push(record([[4, 0x04034B50], ...common]), nameBytes, data);
    central.push(record([[4, 0x02014B50], [2, VERSION], ...common, [2, 0], [2, 0], [2, 0], [4, 0], [4, offset]]), nameBytes);
    offset += 30 + nameBytes.length + size;
  }
  const centralSize = central.reduce((n, part) => n + part.length, 0);
  const end = record([[4, 0x06054B50], [2, 0], [2, 0], [2, files.length], [2, files.length], [4, centralSize], [4, offset], [2, 0]]);
  return new Blob([...local, ...central, end], { type: 'application/zip' });
}
