const hamburger = document.querySelector('.hamburger');
const contents = document.querySelector('.hamburger-contents');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
})

// 문서 전체에 클릭 이벤트 리스너 추가
document.addEventListener('click', (event) => {
    // 클릭된 요소가 hamburger contents 내부에 속하는지 확인
    let clickedInsideEditContainer = false;
    
    if (contents.contains(event.target) || event.target.classList.contains('hamburger')) {
        clickedInsideEditContainer = true;
    }

    // 클릭된 요소가 editContainer 내부에 속하지 않는 경우 모든 editContainer의 'active' 클래스 제거
    if (!clickedInsideEditContainer) {
        hamburger.classList.remove('active');
    }
});


// dark mode toggle
const darkBtn = document.querySelector('.menu-right__darkmode');

darkBtn.addEventListener('click', () => {
    darkBtn.classList.toggle('dark');
    if(darkBtn.classList.contains('dark')){
        darkBtn.querySelector('i').classList.remove('gg-moon');
        darkBtn.querySelector('i').classList.add('gg-sun');
        darkBtn.querySelector('span').innerHTML = 'Light Mode';
    }else{
        darkBtn.querySelector('i').classList.remove('gg-sun');
        darkBtn.querySelector('i').classList.add('gg-moon');
        darkBtn.querySelector('span').innerHTML = 'Dark Mode';
    }
})