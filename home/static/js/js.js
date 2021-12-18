// ======================= contact us form validation
//assigning variables
const form = document.getElementById("form");
const username = document.getElementById("username");
const number = document.getElementById("number");
const email = document.getElementById("email");
const msg = document.getElementById("msg");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  determineValidity();
});
function determineValidity() {
  // get values of the inputs
  const usernameValue = username.value.trim();
  const numberValue = number.value.trim();
  const emailValue = email.value.trim();
  const msgValue = msg.value.trim();

  // array to hold form input values with errors
  const inputErrors = [];

  if (usernameValue === "") {
    // show the error
    adjustError(username, "You have a name, tell us.");
    // add class of error

    // add input value to input errors array
    inputErrors.push(username);
  } else {
    // add class of success
    adjustSuccess(username);
  }
  if (numberValue === "") {
    // show the error
    adjustError(number, "You have a number, write it.");
    // add class of error

    // add input value to input errors array
    inputErrors.push(number);
  } else {
    // add class of success
    adjustSuccess(number);
  }
  if (emailValue === "") {
    // show the error
    adjustError(email, "You have an email, write it.");
    // add class of error

    // add input value to input errors array
    inputErrors.push(email);
  } else {
    // add class of success
    adjustSuccess(email);
  }
  if (msgValue === "") {
    // show the error
    adjustError(msg, "Come on, tell us something.");
    // add class of error

    // add input value to input errors array
    inputErrors.push(msg);
  } else {
    // add class of success
    adjustSuccess(msg);
  }

  // submit form if there are no errors
  if (!inputErrors.length) {
    form.submit();
  }
}
// function to set error message
function adjustError(input, message) {
  const control = input.parentElement; //this is the .controller div
  const errorMsg = control.querySelector("small");
  // display the error message in the small tag
  errorMsg.innerText = message;
  // add the error class
  control.className = "controller error";
  console.log(control);
}
// function to set success
function adjustSuccess(input) {
  const control = input.parentElement;
  control.className = "controller success";
}
