    const date = new Date(),
        ftCopy = document.querySelector("#ft-copy"),
        nav = document.querySelector(".navbar")

    ftCopy.textContent = date.getFullYear()
    window.onscroll = function(){
        if(document.documentElement.scrollTop > 100){
            nav.classList.add("header-scrolled")
        }else nav.classList.remove("header-scrolled")
    }  
