/* kit.js — فقط کمک‌کنندهٔ ردپا روی مسیر (اختیاری). مسیر طی‌شده: ردپا هر ~۲۶ واحد. */
(function(){
  window.KitPath = {
    footprints: function(pathEl, host, vbW, vbH, step){
      step = step || 30;
      var L = pathEl.getTotalLength(), i = 0, side = 1;
      for (var d = 22; d < L - 22; d += step, side = -side, i++){
        var p = pathEl.getPointAtLength(d), q = pathEl.getPointAtLength(d + 2);
        var a = Math.atan2(q.y - p.y, q.x - p.x);
        var x = p.x + Math.cos(a + Math.PI/2) * 3.2 * side, y = p.y + Math.sin(a + Math.PI/2) * 3.2 * side;
        var f = document.createElement('i'); f.className = 'foot';
        f.style.left = (x / vbW * 100) + '%'; f.style.top = (y / vbH * 100) + '%';
        f.style.transform = 'translate(-50%,-50%) rotate(' + (a * 180 / Math.PI + 90) + 'deg)';
        host.appendChild(f);
      }
    }
  };
  document.querySelectorAll('[data-footprints]').forEach(function(el){
    var land = el.closest('.land'), vb = el.ownerSVGElement.viewBox.baseVal;
    window.KitPath.footprints(el, land, vb.width, vb.height);
  });
})();
