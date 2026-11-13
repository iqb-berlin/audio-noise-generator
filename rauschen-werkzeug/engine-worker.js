// Web worker that runs the FFmpeg core for engine.js. One message in, one answer out, plus LOG messages.
// The offline build (maintenance/build_offline.py) removes the import below and puts the core in front of this file.
import createFFmpegCore from './lib/core/ffmpeg-core.js';

let ffmpeg = null;

const handlers = {
  async LOAD({ module }) {
    ffmpeg = await createFFmpegCore({
      // Use the module compiled in the page instead of fetching the .wasm file again
      instantiateWasm(imports, receive) {
        WebAssembly.instantiate(module, imports).then(instance => receive(instance, module));
        return {};
      },
    });
    ffmpeg.setLogger(data => self.postMessage({ type: 'LOG', data }));
    return true;
  },
  EXEC({ args, timeout }) {
    ffmpeg.setTimeout(timeout);
    ffmpeg.exec(...args);
    const ret = ffmpeg.ret;
    ffmpeg.reset();
    return ret;
  },
  WRITE_FILE({ path, data }) { ffmpeg.FS.writeFile(path, data); return true; },
  READ_FILE({ path }) { return ffmpeg.FS.readFile(path); },
  DELETE_FILE({ path }) { ffmpeg.FS.unlink(path); return true; },
};

self.onmessage = async ({ data: { id, type, data } }) => {
  try {
    if (!(type in handlers)) throw new Error('unknown message type');
    if (type !== 'LOAD' && !ffmpeg) throw new Error('ffmpeg is not loaded');
    const out = await handlers[type](data);
    self.postMessage({ id, type, data: out }, out instanceof Uint8Array ? [out.buffer] : []);
  } catch (e) {
    self.postMessage({ id, type: 'ERROR', data: e.toString() });
  }
};
