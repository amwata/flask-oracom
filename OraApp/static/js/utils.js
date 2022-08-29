
let pass = true

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

// function for toggling password vissibility
const togglePasswd = (e, el)=>{
    const pwrd = document.querySelector(el)
    fa = e.querySelector('.fa')

    if(pass){
        fa.classList.replace("fa-eye", "fa-eye-slash")
        pwrd.setAttribute("type", "text")
    }else{
        fa.classList.replace("fa-eye-slash", "fa-eye")
        pwrd.setAttribute("type", "password")
    }pass = !pass
    pwrd.focus()
}

const toggleNav = () => {
	const toggle = document.querySelector(".admin-nav-toggler"),
	 nav = document.querySelector(".admin-nav"),
          main = document.querySelector(".admin-main")
          toggle.classList.toggle("active")
          nav.classList.toggle("active")
          main.classList.toggle("active")
}