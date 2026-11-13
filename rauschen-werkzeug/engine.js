// Runs the FFmpeg core (lib/core/) in a web worker and offers exactly the calls the tool needs.
// The message protocol follows @ffmpeg/ffmpeg 0.12 (MIT, Copyright (c) 2019 Jerome Wu), reduced and rewritten.
// The page compiles the WebAssembly module once and hands it to every new worker, so starting a fresh
// FFmpeg per file only takes a fraction of a second.
//
// The offline build (maintenance/build_offline.py) inlines this file and replaces the block between the
// two "loaders" comments: there the worker and the core come from text embedded in the page.

// <loaders>
const loaders = {
  worker: () => new Worker(new URL('./engine-worker.js', import.meta.url), { type: 'module' }),
  async wasm() {
    const res = await fetch(new URL('./lib/core/ffmpeg-core.wasm', import.meta.url));
    if (!res.ok) throw new Error(`ffmpeg-core.wasm: HTTP ${res.status}`);
    // compileStreaming needs the server to send application/wasm; otherwise compile from the bytes
    return (res.headers.get('content-type') || '').startsWith('application/wasm')
      ? WebAssembly.compileStreaming(res)
      : WebAssembly.compile(await res.arrayBuffer());
  },
};
// </loaders>

let wasmModule = null;
function getWasmModule() {
  wasmModule ??= loaders.wasm().catch(e => { wasmModule = null; throw e; });   // allow a retry after a failure
  return wasmModule;
}

export class FFmpeg {
  #worker = null; #pending = new Map(); #nextId = 0; #logListeners = [];

  on(event, listener) { if (event === 'log') this.#logListeners.push(listener); }

  async load() {
    const module = await getWasmModule();
    this.#worker = loaders.worker();
    this.#worker.onmessage = ({ data: { id, type, data } }) => {
      if (type === 'LOG') { this.#logListeners.forEach(f => f(data)); return; }
      const p = this.#pending.get(id);
      if (!p) return;
      this.#pending.delete(id);
      if (type === 'ERROR') p.reject(new Error(data)); else p.resolve(data);
    };
    // If the worker crashes, pending calls fail instead of hanging forever
    this.#worker.onerror = e => this.#rejectAll(new Error(e.message || 'Der Hintergrundprozess ist abgestürzt'));
    return this.#send('LOAD', { module });
  }

  exec(args, timeout = -1) { return this.#send('EXEC', { args, timeout }); }
  writeFile(path, data) { return this.#send('WRITE_FILE', { path, data }, [data.buffer]); }
  readFile(path) { return this.#send('READ_FILE', { path }); }
  deleteFile(path) { return this.#send('DELETE_FILE', { path }); }

  terminate() {
    this.#rejectAll(new Error('called FFmpeg.terminate()'));
    if (this.#worker) { this.#worker.terminate(); this.#worker = null; }
  }

  #send(type, data, transfer = []) {
    if (!this.#worker) return Promise.reject(new Error('ffmpeg is not loaded'));
    return new Promise((resolve, reject) => {
      const id = this.#nextId++;
      this.#pending.set(id, { resolve, reject });
      this.#worker.postMessage({ id, type, data }, transfer);
    });
  }

  #rejectAll(err) {
    for (const p of this.#pending.values()) p.reject(err);
    this.#pending.clear();
  }
}
