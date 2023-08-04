// // 글자수세기 기능
// document.addEventListener("DOMContentLoaded", function () {
//   const textarea = document.getElementById("proflie-description");
//   const label = document.querySelector(".profile-description__label p");

//   textarea.addEventListener("input", function () {
//     const text = textarea.value;
//     const remainingChars = text.length;

//     // 남은 글자 수를 업데이트
//     label.textContent = `${remainingChars}/100`;

//     // 글자 수가 100자를 초과하면 입력을 막음
//     if (remainingChars < 0) {
//       textarea.value = text.slice(0, 100);
//       label.textContent = "0/100";
//     }
//   });
// });
