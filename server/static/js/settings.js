// 소개란 수정 시 ajax 처리
const introduceUpdate = async (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);
  const introduceArea = document.querySelector("#proflie-description");
  formData.append("proflie-description", introduceArea.value);

  const url = "/main/settings/update_introduce/";
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result: result } = await res.json();
};

// 이메일 알람, 계정 공개 여부, 언어 선택 ajax 처리
const updateProfile = async (inputElement) => {
  const value = inputElement.value;
  const name = inputElement.name;
  const formData = new FormData();
  formData.append("type", name);
  formData.append("radio", value);

  const url = "/main/settings/update_profile/";
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result: result } = await res.json();
};

// 비밀번호 변경 ajax
const changePassword = async (event) => {
  event.preventDefault();

  const formData = new FormData(event.target);

  const url = "/main/settings/change_password/";
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result } = await res.json();
  changepwError(result);
};
const changepwError = (result) => {
  const current_input = document.querySelector("#current-password");
  const new_input = document.querySelector("#new-password");
  const new_check_input = document.querySelector("#new-password-check");
  const errorMessageCodeElement = document.querySelector("#cpw-error-message");
  const successMessageCodeElement = document.querySelector(
    "#cpw-success-message"
  );

  errorMessageCodeElement.textContent = "";
  successMessageCodeElement.textContent = "";
  current_input.classList.remove("error");
  current_input.classList.remove("success");
  new_input.classList.remove("error");
  new_input.classList.remove("success");
  new_check_input.classList.remove("error");
  new_check_input.classList.remove("success");

  if (result == -1) {
    errorMessageCodeElement.textContent = "유효하지 않은 사용자입니다.";
  } else if (result == 0) {
    successMessageCodeElement.textContent = "비밀번호가 변경되었습니다!";
    current_input.classList.add("success");
    new_input.classList.add("success");
    new_check_input.classList.add("success");
  } else if (result == 1) {
    errorMessageCodeElement.textContent = "현재 비밀번호와 다릅니다.";
    current_input.classList.add("error");
  } else if (result == 2) {
    errorMessageCodeElement.textContent = "비밀번호가 틀립니다.";
    new_input.classList.add("error");
    new_check_input.classList.add("error");
  }
};

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

// 네비게이션 바 클릭 이벤트

function onNavigationClick(elementClassName) {
  //   alert(elementClassName);
  const menuContainer = document.querySelector(".settings-menu__container");
  const barIcons = menuContainer.querySelectorAll(".bar-icon");

  barIcons.forEach((barIcon) => {
    if (
      barIcon.parentElement.parentElement.parentElement.className ===
      elementClassName
    ) {
      barIcon.classList.remove("hidden");
    } else {
      barIcon.classList.add("hidden");
    }
  });
}


// mobile 화면에서 소개란 row 3으로
if (window.matchMedia("(max-width: 600px)").matches){
  document.querySelector('.profile-description__textarea > textarea').setAttribute('rows', '3');
}