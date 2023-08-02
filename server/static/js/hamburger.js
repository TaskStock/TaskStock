const hamburger = document.querySelector('.menu-right__hamburger');
const menu_right = document.querySelector('.menu-right');
hamburger.addEventListener('click', () => {
    menu_opened = menu_right.classList
    
    if (menu_opened.contains('active')){
        menu_right.style.width = '0';
    }else{
        menu_right.style.width = '260px';
    }
    menu_opened.toggle('active');
    
})