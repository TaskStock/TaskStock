// 두번째 섹션 - 기능설명
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
  hoverImage("Plan your day.", "Everything you need, all in one place.");
});

landingImgs[1].addEventListener("mouseenter", () => {
  hoverImage(
    "Stay on top of your week.",
    "The timeline shows your week and beyond."
  );
});

landingImgs[2].addEventListener("mouseenter", () => {
  hoverImage(
    "See your month at a glance.",
    "The graph lights up your busy day."
  );
});
