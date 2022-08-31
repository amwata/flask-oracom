
let pass = true,
    mtag = document.querySelector("meta[name=theme-color]"),
    light = "#DDE1E4",
    dark = "#222831"

const bool_IsInView = (el, p, d = true) => {
    const percentVisible = p/100,
    {top:elemTop, bottom:elemBottom, height:elemHeight} = el.getBoundingClientRect(),
    overhang = elemHeight * (1 - percentVisible)
    
    if(!d){return (elemTop >= -overhang && elemBottom <= window.innerHeight + overhang)}
    return elemBottom <= window.innerHeight + overhang
}

const SlideUpOnView = (el, bool) => {
    if(bool_IsInView(el, 50, bool)){
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

// Admin side navbar toggler function
const toggleNav = () => {
	const toggle = document.querySelector(".admin-nav-toggler"),
	 nav = document.querySelector(".admin-nav"),
          main = document.querySelector(".admin-main")
          toggle.classList.toggle("active")
          nav.classList.toggle("active")
          main.classList.toggle("active")
}

// Theme to Dark
const toDark = () => {
    document.documentElement.setAttribute("data-theme", "dark")
    mtag.content = dark
    localStorage.setItem("data-theme", 'dark')

}

// Theme to Light
const toLight = () => {
    document.documentElement.setAttribute("data-theme", "light")
    mtag.content = light
    localStorage.setItem("data-theme", 'light')

}


// Admin Theme toggler function
const toggleTheme = () => {
	const ctn = document.querySelector(".theme-toggler"),
	    lbl = ctn.querySelector(".fa")
    let pref = localStorage.getItem('data-theme')

    if (pref ==='light'){
        lbl.classList.remove("fa-moon-o")
        lbl.classList.add("fa-sun-o")
        toDark()
    }else{
        lbl.classList.remove("fa-sun-o")
        lbl.classList.add("fa-moon-o")
        toLight()
    }    

}


