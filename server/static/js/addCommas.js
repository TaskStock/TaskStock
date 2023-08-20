function addCommasToNumber(number) {
    let numStr = number.toString();
    // 소수점을 기준으로 숫자 나눔
    let parts = numStr.split(".");
    
    // 정수 부분에 콤마 추가
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    
    // 다시 합치고 반환
    return parts.join(".");
}
