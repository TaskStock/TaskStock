const onClickSearch = async () => {
  const url = "/main/search_users/";
  let inputTag = document.querySelector(".search-form input");
  let inputVal = inputTag.value;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: JSON.stringify({
      search_content: inputVal,
    }),
  });
  const { filtered_users: filtered_usersusers } = await res.json();
  searchHandleResponse(filtered_usersusers);
};
