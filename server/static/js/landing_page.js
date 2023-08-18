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
    "To-Do 작성을 통해 당신의 목표를 계획해보세요."
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
