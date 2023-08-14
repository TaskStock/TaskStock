// 검색 창에 입력할 때마다 ajax로 유저 목록
document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.querySelector("#search_content");

  textarea.addEventListener("input", function () {
    const liveChartInput = document.querySelector("#live-chart");
    if (textarea.value == "") liveChartInput.classList.remove("displayNone");
    else liveChartInput.classList.add("displayNone");
    searchAjax(textarea.value);
  });
});

const searchAjax = async (text) => {
  const formData = new FormData();
  formData.append("text", text);

  const url = "/main/group/search_group/ajax/";
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { groups } = await res.json();
  showUserList(groups);
};
const showUserList = (groups) => {
  const currentInput = document.querySelector(
    "#search-users__result-container"
  );
  currentInput.innerHTML = "";

  const my_group = document.getElementById("my_group_name")
    ? document.getElementById("my_group_name").textContent
    : null;

  // users가 [] 인 경우 빈 배열이므로 null이 아님
  if (groups.length > 0) {
    for (const group of groups) {
      atagInput = document.createElement("a");
      atagInput.href = "/main/group/" + group.pk + "/";

      const addButtonContent = group.name == my_group ? "CANCEL" : "FOLLOW";

      atagInput.innerHTML = `
                <div class="search-result__container">
                        <div class="search-result__right--container">
                            <div class="friend-info--pic"></div>
                            <div class="search-result__name-container">
                                <h2>${group.name}</h2>
                                <p>${group.price}</p>
                            </div>
                        </div>
                        <div class="search-result__right-container">
                            <div class="search-result__info">
                                <div class="search-result__right-upper-container">
                                    <form onsubmit="handleFollowButtonClick(event)">
                                        <input type="hidden" name="group" value="${group.name}">
                                        <button type="submit" name="group-button" class="add-button">${addButtonContent}</button>
                                    </form>
                                </div>
                                <p>${group.create_user}</p>
                            </div>                           
                        </div>    
                    </div>
                `;
      currentInput.appendChild(atagInput);
    }
  }
};

// create 부분

const handleCreateButtonClick = async (event) => {
  event.preventDefault();

  const input_content = document.querySelector("#create-input").value;
  console.log(input_content);
  const url = "/main/group/create_group/";

  const formData = new FormData(event.target);
  formData.append("name", input_content);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result: result } = await res.json();
  handleCreateResult(result);
};

const handleCreateResult = async (result) => {
  if (result == "Exist") {
    alert("그룹은 1개만 가능합니다.");
  } else {
    alert("그룹이 생성되었습니다.");
  }
};

// follow 부분

const handleFollowButtonClick = async (event) => {
  const addButton_text = event.target.querySelector(
    "[name=group-button]"
  ).textContent; // Get the button element
  const groupInput = event.target.querySelector("[name=group]"); // Get the input element
  const group = groupInput.value; // Get the value of the input element
  event.preventDefault();

  console.log(group);
  console.log(addButton_text.trim());
  const url = "/main/group/follow_group/";

  const formData = new FormData(event.target);
  formData.append("buttonText", addButton_text.trim());
  formData.append("group", group);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { text, name, price, create_user, pk } = await res.json();
  handleFollowButtonText(text, name, price, create_user, pk, event);
};
const handleFollowButtonText = async (
  text,
  name,
  price,
  create_user,
  pk,
  event
) => {
  const addButton = event.target.querySelector("[name=group-button]");
  if (text === "CANCEL") {
    addButton.textContent = "CANCEL";
    document.querySelector(
      ".my-group__container"
    ).innerHTML = `<a href="/main/group/${pk}/">
    <div class="search-result__container">
        <div class="search-result__right--container">
            <div class="friend-info--pic"></div>
            <div class="search-result__name-container">
                <h2>${name}</h2>
                <p>${price}</p>
            </div>
        </div>
        <div class="search-result__right-container">
            <div class="search-result__info">
                <div class="search-result__right-upper-container">
                    <form onsubmit="handleFollowButtonClick(event)">
                        <input type="hidden" name="group" value="${name}">
                        <button type="submit" name="group-button" class="add-button">CANCEL</button>
                    </form>
                </div>
                <p>${create_user}</p>
            </div>
            
        </div>    
    </div>
</a>`;
  } else if (text === "FOLLOW") {
    addButton.textContent = "FOLLOW";
    document.querySelector(".my-group__container").innerHTML = `
    <span>가입 그룹이 없습니다.</span>
    `;
  }
};
