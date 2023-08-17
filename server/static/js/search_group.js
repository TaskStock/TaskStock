// 검색 창에 입력할 때마다 ajax로 유저 목록
document.addEventListener("DOMContentLoaded", function () {
  const textInput = document.querySelector("#search-group_content");
  console.log(textInput);
  textInput.addEventListener("input", function () {
    const liveGroupChartInput = document.querySelector("#live-group-chart");
    if (textInput.value == "")
      liveGroupChartInput.classList.remove("displayNone");
    else liveGroupChartInput.classList.add("displayNone");
    searchGroupAjax(textInput.value);
  });
});

// 입력한 text에 해당하는 유저 목록을 가져오는 ajax 처리
const searchGroupAjax = async (text) => {
  const formData = new FormData();
  formData.append("textContent", text);

  const url = "/main/group/search_group/ajax/";
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { groups } = await res.json();
  showGroupsList(groups);
};
const showGroupsList = (groups) => {
  const currentInput = document.querySelector(
    "#search-groups__result-container"
  );
  currentInput.innerHTML = "";

  // 내 그룹인지 여부에 따라 버튼 내용이 달라짐
  const my_group = document.getElementById("my_group_name")
    ? document.getElementById("my_group_name").textContent
    : null;

  // users가 [] 인 경우 빈 배열이므로 null이 아님
  if (groups.length > 0) {
    for (const group of groups) {
      divtagInput = document.createElement("div");
      divtagInput.classList.add("search-group-result__container");
      const href = `/main/group/${group.pk}/`;

      const addButtonContent =
        group.name == my_group ? "LEAVE GROUP" : "JOIN GROUP";

      const inputForm =
        addButtonContent == "JOIN GROUP"
          ? '<input type="text" name="group-password-verify-input" id="password-verify-input">'
          : "";

      // 검색 결과를 보여주는 부분
      divtagInput.innerHTML = `
        <div class="search-group-result__right--container">
            <div class="friend-group-info--pic"></div>
            <a href="${href}">
              <div class="search-group-result__name-container">
                  <h2>${group.name}</h2>
                  <p>${group.price}</p>
              </div>
            </a>
        </div>
        <div class="search-group-result__right-container">
            <div class="search-group-result__info">
                <div class="search-group-result__right-upper-container">
                    <form onsubmit="handleFollowButtonClick(event)">
                        <input type="hidden" name="group" value="${group.name}">
                        ${inputForm}
                        <button type="submit" name="group-button" class="add-button">${addButtonContent}</button>
                    </form>
                </div>
                <p>${group.create_user}</p>
            </div>                           
        </div>    
                `;
      currentInput.appendChild(divtagInput);
    }
  }
};

// create 부분

const handleCreateButtonClick = async (event) => {
  event.preventDefault();

  const name_content = document.querySelector("#name-input").value;
  const password_content = document.querySelector("#password-input").value;

  const url = "/main/group/create_group/";

  const formData = new FormData(event.target);
  formData.append("name", name_content);
  formData.append("password", password_content);

  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result: result } = await res.json();
  handleCreateResult(result);
};

const handleCreateResult = async (result) => {
  if (result == "my_group_exist") {
    alert("그룹은 1개만 가능합니다.");
  } else if (result == "group_name_exist") {
    alert("그룹명이 이미 존재합니다.");
  } else {
    alert("그룹이 생성되었습니다.");
    window.location.reload();
  }
};

// follow 부분

const handleFollowButtonClick = async (event) => {
  event.preventDefault();
  if (
    event.target.querySelector("[name=group-button]").textContent ===
    "LEAVE GROUP"
  ) {
    if (window.confirm("정말 탈퇴하시겠습니까?")) {
      handleButtonClickSend(event);
    }
  } else {
    handleButtonClickSend(event);
  }
};

const handleButtonClickSend = async (event) => {
  const addButton_text = event.target.querySelector(
    "[name=group-button]"
  ).textContent; // Get the button element
  const groupInput = event.target.querySelector("[name=group]"); // Get the input element
  const group = groupInput.value; // Get the value of the input element
  const passwordInput = event.target.querySelector(
    "[name=group-password-verify-input]"
  ); // Get the input element
  event.preventDefault();

  const password = passwordInput ? passwordInput.value : null; // 값이 존재하지 않으면 null 반환

  console.log(group);
  console.log(addButton_text.trim());
  const url = "/main/group/follow_group/";

  const formData = new FormData(event.target);
  formData.append("group-button", addButton_text.trim());
  formData.append("group", group);
  formData.append("password", password);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { text } = await res.json();
  handleFollowButtonText(text, event);
};
const handleFollowButtonText = async (text, event) => {
  console.log(text);
  const addButton = event.target.querySelector("[name=group-button]");
  if (text === "LEAVE GROUP") {
    alert("그룹에 가입되었습니다.");
    addButton.textContent = "LEAVE GROUP";
    // 그룹원 수 감소 리로드를 통해
    window.location.reload();
  } else if (text === "JOIN GROUP") {
    alert("그룹에서 탈퇴되었습니다.");
    addButton.textContent = "JOIN GROUP";
    // 그룹원 수 증가 리로드를 통해
    window.location.reload();
  } else if (text === "WRONG PASSWORD") {
    alert("비밀번호가 틀렸습니다.");
  } else if (text == "ALREADY JOINED") {
    alert("이미 가입된 그룹이 존재합니다.");
  }
};
