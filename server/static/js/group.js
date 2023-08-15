// follow부분

// ADD,DELETE 버튼을 클릭 했을 때 ajax 통신을 통해 그룹원 추가, 삭제
const handleButtonClick = async (event) => {
  const addButton = document.querySelector("#add-button");
  const group = document.querySelector(".group-content__name").textContent;
  event.preventDefault();

  const url = "/main/group/follow_group/";

  const formData = new FormData(event.target);
  formData.append("group-button", addButton.textContent);
  formData.append("group", group);
  const res = await fetch(url, {
    method: "POST",
    headers: {},
    body: formData,
  });
  const { text: text } = await res.json();

  console.log(text);
  handleButtonText(text);
};

const handleButtonText = async (Text) => {
  if (Text === "DELETE GROUP") {
    document.querySelector("#add-button").textContent = "DELETE GROUP";
    // 그룹원 수 감소 리로드를 통해
    window.location.reload();
  } else if (Text === "ADD GROUP") {
    document.querySelector("#add-button").textContent = "ADD GROUP";
    // 그룹원 수 증가 리로드를 통헤
    window.location.reload();
  }
};

// update 부분
// 그룹의 이름을 업데이트 시킨다

// yes,no 창을 띄움
const confirmModal = async (event) => {
  console.log(event);
  event.preventDefault();
  if (window.confirm("정말 이름을 변경하시겠습니까?")) {
    handleUpdateButtonClick(event);
  } else {
    console.log("취소. 변화 없음");
    window.location.reload();
  }
};

const handleUpdateButtonClick = async (event) => {
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
