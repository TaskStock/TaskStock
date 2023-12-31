// 그룹 생성 active toggle
const createGroupBtn = document.querySelector("#create-group i");

createGroupBtn.addEventListener("click", () => {
  const create_group = document.querySelector(".create-group");
  const create_input = create_group.querySelector('#name-input');
  create_group.classList.toggle("active");
  if(create_group.classList.contains('active')){
    setTimeout(() => {
      create_input.focus()
    }, 500);
  }
});

document.addEventListener('click', (event) => {
  const create_show = document.querySelector('.create-group--show');
  let clickedInsideEditContainer = false;

  if (create_show.contains(event.target) || createGroupBtn.contains(event.target)) {
      clickedInsideEditContainer = true;
  }

  if (!clickedInsideEditContainer) {
    document.querySelector(".create-group").classList.remove("active");
  }
});

// mobile 화면 search icon toggle
if (window.matchMedia("(max-width: 500px)").matches) {
  const mb_searchToggleBtn = document.querySelector("#mb-search-btn");
  const mb_searchCancelBtn = document.querySelector("#mb-searchCancel-btn");
  const mb_searchForm = document.querySelector(".search-group-form");
  mb_searchToggleBtn.addEventListener("click", () => {
    // console.log('clicked');
    mb_searchForm.classList.add("active");
    handleSearchToggle();
  });
  mb_searchCancelBtn.addEventListener("click", () => {
    mb_searchForm.classList.remove("active");
    handleSearchToggle();
  });
}
function handleSearchToggle() {
  const searchLogo = document.querySelector(".search-group-header h1");
  const mb_searchForm = document.querySelector(".search-group-form");
  const mb_searchToggleBtn = document.querySelector("#mb-search-btn");
  const mb_searchCancelBtn = document.querySelector("#mb-searchCancel-btn");
  if (mb_searchForm.classList.contains("active")) {
    document.querySelector("#search-group_content").style.display = "block";
    mb_searchCancelBtn.querySelector("i").style.display = "block";
    mb_searchToggleBtn.style.display = "none";
    searchLogo.style.display = "none";
  } else {
    document.querySelector("#search-group_content").style.display = "none";
    mb_searchCancelBtn.querySelector("i").style.display = "none";
    mb_searchToggleBtn.style.display = "block";
    searchLogo.style.display = "block";
  }
}

// 검색 창에 입력할 때마다 ajax로 유저 목록
document.addEventListener("DOMContentLoaded", function () {
  const textInput = document.querySelector("#search-group_content");
  textInput.addEventListener("input", function () {
    const liveGroupChartInput = document.querySelector(
      ".search-group--contents"
    );
    const searchContainer = document.querySelector(".search-group-users");

    if (textInput.value == "") {
      liveGroupChartInput.classList.remove("displayNone");
      searchContainer.classList.add("displayNone");
    } else {
      liveGroupChartInput.classList.add("displayNone");
      searchContainer.classList.remove("displayNone");
      searchGroupAjax(textInput.value);
    }
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

      const addButtonContent = group.name == my_group ? "탈퇴" : "가입";

      // 검색 결과를 보여주는 부분
      divtagInput.innerHTML = `
      
            <div class="search-group__header">
                <a href="${href}">
                    <h2>${group.name}</h2>
                </a>
                <form onsubmit="handleFollowButtonClick(event)">
                    <input type="hidden" name="group" value="${group.name}">
                    <button type="submit" name="group-button" class="add-button">${addButtonContent}</button>
                </form>
            </div>
            <p>
                <i class="fa-solid fa-won-sign"></i>
                <span>${group.price}</span>
            </p>
            <p>
                <i class="fa-solid fa-user"></i>
                <span>${group.member_cnt}</span>
            </p>
            <p>
                <i class="fa-solid fa-user-tie"></i>
                <span>${group.create_user}</span>
            </p>
        
                `;
      currentInput.appendChild(divtagInput);
    }
  }
};

// create 부분

const handleCreateButtonClick = async (event) => {
  event.preventDefault();

  const name_content = document.querySelector("#name-input").value;

  const url = "/main/group/create_group/";

  const formData = new FormData(event.target);
  formData.append("name", name_content);

  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result: result } = await res.json();
  handleCreateResult(result);
  document.querySelector(".create-group").classList.remove("active");
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
  const buttonText = event.target.querySelector(
    "[name=group-button]"
  ).textContent;
  if (buttonText.trim() == "가입") {
    handleButtonClickSend(event);
  } else {
    if (window.confirm("정말 탈퇴하시겠습니까?")) {
      handleButtonClickSend(event);
    }
  }
};

const handleButtonClickSend = async (event) => {
  const addButton_text = event.target.querySelector(
    "[name=group-button]"
  ).textContent; // Get the button element
  const groupInput = event.target.querySelector("[name=group]"); // Get the input element
  const group = groupInput.value; // Get the value of the input element
  event.preventDefault();

  const url = "/main/group/follow_group/";

  const formData = new FormData(event.target);
  formData.append("group-button", addButton_text.trim());
  formData.append("group", group);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { text } = await res.json();
  handleFollowButtonText(text, event);
};
const handleFollowButtonText = async (text, event) => {
  const addButton = event.target.querySelector("[name=group-button]");
  if (text === "탈퇴") {
    alert("그룹에 가입되었습니다.");
    addButton.textContent = "탈퇴";
    // 그룹원 수 감소 리로드를 통해
    window.location.reload();
  } else if (text === "가입") {
    alert("그룹에서 탈퇴되었습니다.");
    addButton.textContent = "가입";
    // 그룹원 수 증가 리로드를 통해
    window.location.reload();
  } else if (text == "ALREADY JOINED") {
    alert("이미 가입된 그룹이 존재합니다.");
  }
};

if (window.matchMedia("(max-width: 500px)").matches) {
  handleSearchToggle();
}

// comma 찍기
if(document.querySelector('.my-group__container')){
  const myGroup = document.querySelector('.my-group__container');
  const top10 = document.querySelector('.group-top10__container');
  const myGroup_delta = myGroup.querySelector('a p:nth-of-type(1) span');
  const myGroup_price = myGroup.querySelector('a p:nth-of-type(2) span');
  const top10_delta = top10.querySelector('p:nth-of-type(1) span');
  const top10_price = top10.querySelector('p:nth-of-type(2) span');

  const display_myGroup_delta = addCommasToNumber(myGroup_delta.innerText);
  const display_myGroup_price = addCommasToNumber(myGroup_price.innerText);
  const display_top10_delta = addCommasToNumber(top10_delta.innerText);
  const display_top10_price = addCommasToNumber(top10_price.innerText);

  myGroup_delta.innerHTML = `${display_myGroup_delta} ₩`;
  myGroup_price.innerHTML = `${display_myGroup_price} ₩`;
  top10_delta.innerHTML = `${display_top10_delta} ₩`;
  top10_price.innerHTML = `${display_top10_price} ₩`;
}

