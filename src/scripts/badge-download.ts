// Store-only ZIP keeps downloads local and avoids sending artwork to a service.
function zip(files: { name: string; bytes: Uint8Array }[]): Blob {
  const parts: Uint8Array[] = [], entries: Uint8Array[] = [];
  let offset = 0;
  for (const file of files) {
    const name = new TextEncoder().encode(file.name);
    let crc = 0xffffffff;
    for (const byte of file.bytes) {
      crc ^= byte;
      for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ (0xedb88320 & -(crc & 1));
    }
    crc = (crc ^ 0xffffffff) >>> 0;
    const header = new Uint8Array(30 + name.length);
    const view = new DataView(header.buffer);
    view.setUint32(0,0x04034b50,true); view.setUint16(4,20,true);
    view.setUint32(14,crc,true); view.setUint32(18,file.bytes.length,true); view.setUint32(22,file.bytes.length,true);
    view.setUint16(26,name.length,true); header.set(name,30);
    parts.push(header,file.bytes);
    const entry=new Uint8Array(46+name.length), directory=new DataView(entry.buffer);
    directory.setUint32(0,0x02014b50,true); directory.setUint16(4,20,true); directory.setUint16(6,20,true);
    directory.setUint32(16,crc,true); directory.setUint32(20,file.bytes.length,true); directory.setUint32(24,file.bytes.length,true);
    directory.setUint16(28,name.length,true); directory.setUint32(42,offset,true); entry.set(name,46);
    entries.push(entry); offset+=header.length+file.bytes.length;
  }
  const size=entries.reduce((sum,entry)=>sum+entry.length,0);
  const end=new Uint8Array(22), view=new DataView(end.buffer);
  view.setUint32(0,0x06054b50,true); view.setUint16(8,files.length,true); view.setUint16(10,files.length,true);
  view.setUint32(12,size,true); view.setUint32(16,offset,true);
  return new Blob([...parts,...entries,end] as BlobPart[],{type:'application/zip'});
}

async function transparentPrint(url: string): Promise<Blob> {
  const image=new Image(); image.src=url;
  await image.decode();
  const canvas=document.createElement('canvas'); canvas.width=1200; canvas.height=1688;
  const ctx=canvas.getContext('2d');
  if (!ctx) throw new Error('Canvas unavailable');
  ctx.beginPath(); ctx.roundRect(0,0,1200,1688,50); ctx.clip();
  ctx.drawImage(image,0,0,1200,1688);
  // The punched slot, like the area outside the rounded card, is transparent.
  ctx.globalCompositeOperation='destination-out';
  ctx.beginPath(); ctx.roundRect(468,64,264,48,24); ctx.fill();
  return new Promise((resolve,reject)=>canvas.toBlob(blob=>blob?resolve(blob):reject(new Error('PNG export failed')),'image/png'));
}

export function initBadgeDownload(): void {
  const dialog=document.querySelector<HTMLDialogElement>('[data-download-dialog]');
  if (!dialog) return;
  const trigger=document.querySelector<HTMLButtonElement>('[data-download-pass]');
  const status=dialog.querySelector<HTMLElement>('[data-download-status]')!;
  let pending: Promise<void> | null=null;
  const urls: string[]=[];
  trigger?.addEventListener('click',()=>{
    dialog.showModal();
    if (pending) return;
    status.textContent=dialog.dataset.preparing || '';
    pending=(async()=>{
      const faces=await Promise.all(['front','back'].map(async face=>{
        const link=dialog.querySelector<HTMLAnchorElement>(`[data-download-face="${face}"]`)!;
        const blob=await transparentPrint(link.dataset.source!);
        const url=URL.createObjectURL(blob); urls.push(url);
        link.href=url; link.removeAttribute('aria-disabled');
        dialog.querySelector<HTMLImageElement>(`[data-print-preview="${face}"]`)!.src=url;
        return {name:link.download,bytes:new Uint8Array(await blob.arrayBuffer())};
      }));
      const all=dialog.querySelector<HTMLAnchorElement>('[data-download-zip]')!;
      const url=URL.createObjectURL(zip(faces)); urls.push(url);
      all.href=url; all.removeAttribute('aria-disabled');
      status.textContent=dialog.dataset.hint || '';
    })().catch(()=>{status.textContent=dialog.dataset.error || ''; pending=null;});
  });
  dialog.querySelector('[data-download-close]')?.addEventListener('click',()=>dialog.close());
  window.addEventListener('pagehide',()=>urls.forEach(url=>URL.revokeObjectURL(url)));
}
