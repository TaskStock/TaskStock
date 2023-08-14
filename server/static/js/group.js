// follow부분

const handleButtonClick = async (event, name, price) => {
  const addButton = document.querySelector("#add-button");
  const group = document.querySelector(".group-content__name").textContent;
  event.preventDefault();

  const url = "/main/group/follow_group/";

  const formData = new FormData(event.target);
  formData.append("buttonText", addButton.textContent);
  formData.append("group", group);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { text: text } = await res.json();
  let id_name = `group-content__li-${name}`;

  console.log(text, id_name, price, name);
  handleButtonText(text, id_name, price, name);
};

const handleButtonText = async (Text, id_name, price, name) => {
  if (Text === "CANCEL") {
    document.querySelector("#add-button").textContent = "CANCEL";

    // 리스트에 사용자 추가
    const ul = document.querySelector(".group-content__ul");
    const li = document.createElement("li");
    li.setAttribute("id", id_name);
    li.innerHTML = `   
    <div>그룹원 명: ${name}</div>
    <div>그룹원 가격: ${price}</div>`;
    ul.appendChild(li);

    group_member = document.getElementById("group-member");
    group_member = parseInt(group_member.textContent) - 1;
  } else if (Text === "FOLLOW") {
    document.querySelector("#add-button").textContent = "FOLLOW";

    // 리스트에서 사용자 삭제
    document.getElementById(id_name).remove();

    group_member = document.getElementById("group-member");
    group_member = parseInt(group_member.textContent) + 1;
  }
};

// update 부분
const handleUpdateButtonClick = async (event) => {
  event.preventDefault();

  const input_content = document.querySelector("#update-input").value;
  console.log(input_content);
  const url = "/main/group/update_group/";
  const group_name = document.querySelector(".group-content__name").textContent;

  const formData = new FormData(event.target);
  formData.append("update_name", input_content);
  formData.append("group_name", group_name);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { result: result } = await res.json();
  handleUpdateResult(result, input_content);
};

const handleUpdateResult = async (result, updatedGroupName) => {
  if (result == "Exist") {
    alert("그룹명이 이미 존재합니다.");
  } else {
    alert("그룹명이 변경되었습니다.");
    document.querySelector(".group-content__name").textContent =
      updatedGroupName;
    document.querySelector("#update-input").value = "";
  }
};
