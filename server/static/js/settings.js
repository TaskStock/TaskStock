// 페이지 로드 시에 실행
document.addEventListener("DOMContentLoaded", setupTextarea);

// 글자수세기 기능
function setupTextarea() {
  const textarea = document.getElementById("proflie-description");
  const label = document.querySelector(".profile-description__textarea p");

  textarea.addEventListener("input", function () {
    const text = textarea.value;
    const remainingChars = 50 - text.length;

    // 남은 글자 수를 업데이트
    label.textContent = `${text.length}/50`;

    // 글자 수가 50자를 초과하면 입력을 막음
    if (remainingChars < 0) {
      textarea.value = text.slice(0, 50);
      label.textContent = "50/50";
    }
  });
}

function smoothScrollToElement(elementId, event) {
  event.preventDefault();
  const targetElement = document.getElementById(elementId);
  if (targetElement) {
    targetElement.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

