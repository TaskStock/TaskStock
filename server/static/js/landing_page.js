// 두번째 섹션 - 기능설명 클릭 시 변경하는 함수
const landingImgs = document.querySelectorAll(".container-box__imgs__img");
const landingText = document.querySelector(".container-box__text");
const header = landingText.querySelector("h3");
const description = landingText.querySelector("p");

console.log(landingImgs);
console.log(header);
console.log(description);

const hoverImage = (newHeader, newDescription) => {
  header.innerText = newHeader;
  description.innerText = newDescription;
};

// 이미지에 mouse on -> hover한 이미지에 해당되는 설명란으로 내용 변경
landingImgs[0].addEventListener("mouseenter", () => {
  hoverImage(
    "To-Do를 작성해 보세요.",
    "To-Do 작성을 통해 당신의 목표를 계획해보세요.더 많은 To-Do를 완료할 수록 붉은 원이 진해집니다."
  );
});

landingImgs[1].addEventListener("mouseenter", () => {
  hoverImage(
    "주가의 상승을 통해 확인해보세요.",
    "당신의 목표 달성이 주가를 상승시킵니다."
  );
});

landingImgs[2].addEventListener("mouseenter", () => {
  hoverImage(
    "친구들과 공유해보세요.",
    "당신의 목표와 주가를 팔로워들과 함께 공유해보세요."
  );
});

// 그룹,뱃지 호버 이벤트
const imageOne = document.getElementById("image-one");
const imageTwo = document.getElementById("image-two");
const imageThree = document.getElementById("image-three");
const text = document.querySelector(".advertise-box__description h3");

imageOne.addEventListener("mouseenter", () => {
  text.innerHTML =
    "프로젝트를 만들어 보세요. <br><br> 프로젝트 단위로 당신의 목표를 관리할 수 있습니다.";
});
imageTwo.addEventListener("mouseenter", () => {
  text.innerHTML =
    "그룹에 가입해보세요. <br><br> 다른 그룹과 주식 가치를 경쟁할 수 있습니다.";
});
imageThree.addEventListener("mouseenter", () => {
  text.innerHTML =
    "뱃지를 획득해 보세요. <br><br> 숨겨진 많은 뱃지들을 획득할 수 있습니다.";
});
// 기기 이미지 변경 2초마다

const changingImage = document.getElementById("changing-image");

const imageSources = [
  "/static/img/landing-page-4-1-1.PNG",
  "/static/img/landing-page-4-1-2.PNG",
  "/static/img/landing-page-4-1.PNG",
];

let currentImageIndex = 0;

const updateImage = () => {
  currentImageIndex = (currentImageIndex + 1) % imageSources.length;
  changingImage.src = imageSources[currentImageIndex];
};

setInterval(updateImage, 2000);

// page-vision 호버 이벤트
// page-vision 호버 이벤트
const follow = document.getElementById("page-vision__following");
const group = document.getElementById("page-vision__group");
const imageContainer = document.querySelector(".introduction-vision__image");

follow.addEventListener("mouseenter", () => {
  imageContainer.innerHTML =
    '<img src="/static/img/landing-page-6-1-2.PNG" alt="rule image">';
});

group.addEventListener("mouseenter", () => {
  imageContainer.innerHTML =
    '<img src="/static/img/landing-page-6-1-1.PNG" alt="rule image">';
});
