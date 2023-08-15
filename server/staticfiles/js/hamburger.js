const hamburger = document.querySelector('.hamburger');
const contents = document.querySelector('.hamburger-contents');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
})

// 문서 전체에 클릭 이벤트 리스너 추가
document.addEventListener('click', (event) => {
    // 클릭된 요소가 hamburger contents 내부에 속하는지 확인
    let clickedInsideEditContainer = false;
    
    if (contents.contains(event.target) || event.target.parentNode.classList.contains('hamburger') || event.target.classList.contains('hamburger')) {
        clickedInsideEditContainer = true;
    }

    // 클릭된 요소가 editContainer 내부에 속하지 않는 경우 모든 editContainer의 'active' 클래스 제거
    if (!clickedInsideEditContainer) {
        hamburger.classList.remove('active');
    }
});

//  mobile hamburger
const left_section = document.querySelector('section');
const tb_section = document.querySelector('#tb-section');

document.querySelector('#hamburger-tb').addEventListener('click', () => {
    left_section.style.left = '-350px';
    
})
document.querySelector('#tb-hamburger').addEventListener('click', () => {
    left_section.style.left = '0';    
    tb_section.style.left = '-70px';
})

// dark mode toggle
const bodyEl = document.querySelector('body');
const darkBtn = document.querySelector('.menu-right__darkmode');
const activeTheme = localStorage.getItem('theme');

if(activeTheme){
    bodyEl.classList.add('dark');
    darkBtn.querySelector('i').classList.remove('gg-moon');
    darkBtn.querySelector('i').classList.add('gg-sun');
    darkBtn.querySelector('span').innerHTML = 'Light Mode';
}

darkBtn.addEventListener('click', () => {
    bodyEl.classList.toggle('dark');
   
    if(bodyEl.classList.contains('dark')){
        localStorage.setItem('theme', 'dark');
        darkBtn.querySelector('i').classList.remove('gg-moon');
        darkBtn.querySelector('i').classList.add('gg-sun');
        darkBtn.querySelector('span').innerHTML = 'Light Mode';
    }else{
        localStorage.removeItem('theme');
        darkBtn.querySelector('i').classList.remove('gg-sun');
        darkBtn.querySelector('i').classList.add('gg-moon');
        darkBtn.querySelector('span').innerHTML = 'Dark Mode';
    }
})



