window.onload = () =>{
    const hero = document.querySelector("#hero")
    const animate = () =>{
        
        SlideUpOnView(hero, 0)
        raf(animate)
    }
    animate()

}

