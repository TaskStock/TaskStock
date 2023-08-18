const badges = document.querySelectorAll('.badge-container');
const badge_modal = document.querySelector('.badge-modal');

badges.forEach(badge => {
    badge.addEventListener('click', () => {
        // modal 띄우기
        badge_modal.classList.add('modalShow');
        // img, h3, p 저장
        const badgeImg = badge.querySelector('img').getAttribute('src');
        const modalImg = document.createElement('img'); // 새로운 img 요소 생성
        modalImg.setAttribute('src', badgeImg);

        const badgeModalTop = badge_modal.querySelector('.badge-modal--top');
        badgeModalTop.innerHTML = ''; 
        badgeModalTop.appendChild(modalImg); 

        const badgeName = badge.querySelector('h3').innerHTML;
        const badgeExplain = badge.querySelector('p').innerHTML;
        console.log(badgeImg, badgeName, badgeExplain);

        badge_modal.querySelector('.badge-modal--bottom h3').innerHTML = badgeName;
        badge_modal.querySelector('.badge-modal--bottom p').innerHTML = badgeExplain;

        
        
    })
})

document.querySelector('.badge-modal__delBtn').addEventListener('click', () => {
    // 모달 닫기
    badge_modal.classList.remove('modalShow');
})