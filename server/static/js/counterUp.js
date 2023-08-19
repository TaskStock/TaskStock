
// // function counterUp(element, options) {
// //     console.log('element: ', element);
// //     console.log("Initial options:", options);

// //     var settings = Object.assign({
// //         time: 400,
// //         delay: 10
// //     }, options);
// //     console.log("Merged settings:", settings);

// //     var finalValue; // 최종 값을 저장할 변수

// //     var animateNumbers = function() {
// //         console.log("Animating numbers for element:", element);

// //         var numbers = [],
// //             totalTime = settings.time / settings.delay,
// //             textValue = element.textContent,
// //             hasCommas = /[0-9]+,[0-9]+/.test(textValue),
// //             startValue = parseInt(element.textContent.replace(/,/g, ""), 10) || 0;

// //         console.log("Initial text value:", textValue);
// //         console.log("Start value:", startValue);

// //         textValue = textValue.replace(/,/g, "");

// //         var isInteger = /^[0-9]+$/.test(textValue),
// //             isFloat = /^[0-9]+\.[0-9]+$/.test(textValue),
// //             decimalPlaces = isFloat ? (textValue.split(".")[1] || []).length : 0;

// //         for (var i = totalTime; i >= 1; i--) {
// //             var num = startValue + (parseInt(textValue) - startValue) / totalTime * i;
// //             if (isFloat) {
// //                 num = parseFloat(startValue + (parseFloat(textValue) - startValue) / totalTime * i).toFixed(decimalPlaces);
// //             }
// //             if (hasCommas) {
// //                 while (/(\d+)(\d{3})/.test(num.toString())) {
// //                     num = num.toString().replace(/(\d+)(\d{3})/, "$1,$2");
// //                 }
// //             }
// //             numbers.unshift(num);
// //         }

// //         console.log("Animation numbers array:", numbers);

// //         element.dataset.counterupNums = JSON.stringify(numbers);

// //         var updateText = function() {
// //             var nums = JSON.parse(element.dataset.counterupNums);
// //             console.log("Updating text to:", nums[0]);
// //             element.textContent = nums.shift();
// //             element.dataset.counterupNums = JSON.stringify(nums);

// //             // 마지막 숫자를 저장합니다.
// //             if (nums.length === 0) {
// //                 finalValue = element.textContent;
// //             }
// //         };

// //         setTimeout(updateText, settings.delay);
// //     };

// //     var observer = new IntersectionObserver(function(entries, observer) {
// //         entries.forEach(entry => {
// //             if (entry.isIntersecting) {
// //                 animateNumbers();
// //                 observer.disconnect();
// //             }
// //         });
// //     }, {
// //         threshold: 1.0
// //     });

// //     observer.observe(element);

// //     // 최종 값을 반환합니다.
// //     return finalValue;
// // }
// // console.log(document.querySelectorAll('.counter'));

// // function counting(){
// //     document.querySelectorAll('.counter').forEach(c => {
// //         console.log('c:', c.textContent);
// //         let result = counterUp(c, {
// //             delay: 10,
// //             time: 456
// //         });
// //         c.innerHTML = result;
// //     })
// // }
// // counting();
// // console.log(counting());
//     // var element = document.querySelector('.counter');
//     // var result = counterUp(element, {
//     //     time: 400,
//     //     delay: 10
//     // });

//     // 반환된 값을 다른 요소의 innerHTML로 설정합니다.
//     // document.querySelector('.result').innerHTML = result;


// function animateCounter(startValue, endValue, duration = 400, delay = 10) {
//     return new Promise((resolve, reject) => {
//         let currentStep = 0;
//         const totalSteps = duration / delay;
//         const stepValue = (endValue - startValue) / totalSteps;

//         let currentValue = startValue;

//         const interval = setInterval(() => {
//             currentStep++;
//             currentValue += stepValue;
            
//             if (currentStep >= totalSteps) {
//                 clearInterval(interval);
//                 resolve(endValue); // 애니메이션이 끝나면 최종 값을 반환합니다.
//             } else {
//                 console.log(Math.round(currentValue)); // 현재 값을 콘솔에 출력합니다.
//             }
//         }, delay);
//     });
// }

// // 예제 사용:
// animateCounter(0, 100).then(finalValue => {
//     console.log(`Finished counting. Final value: ${finalValue}`);
// });





// function counting(){

//     const element = document.querySelector('#counter_close');
//     console.log('함수 밖 ', element);
//     let result = counterUp(element, {
//         time: 400, 
//         delay: 10
//     });;
    
//     document.querySelector('#counter_close').innerHTML = result;
// }
// setTimeout(counting, 1000);
// // counting();