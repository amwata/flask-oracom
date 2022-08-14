

const bool_IsInView = (el, p, d = true) => {
    const percentVisible = p/100,
    {top:elemTop, bottom:elemBottom, height:elemHeight} = el.getBoundingClientRect(),
    overhang = elemHeight * (1 - percentVisible)
    
    if(!d){return (elemTop >= -overhang && elemBottom <= window.innerHeight + overhang)}
    return elemBottom <= window.innerHeight + overhang
}

const SlideUpOnView = (el, bl) => {
    if(bool_IsInView(el, 50, bl)){
        el.classList.add("inview")
    }
    else el.classList.remove("inview")
}

const raf = requestAnimationFrame || (ts => (setTimeout(ts, 1000/60))),
	cancelRaf = (h) => {
		cancelAnimationFrame ? cancelAnimationFrame(h) : clearTimeout(h)
}