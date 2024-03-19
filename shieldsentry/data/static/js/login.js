const mail1 = document.querySelector("#mail");
const pass1 = document.querySelector("#pass");

const login = document.querySelector("#login");


const checkmail = () => {
  let valid = false;

  const mail = mail1.value.trim();

  if (!isRequired(mail)) {
    showError(mail1, "Email cannot be blank");
  } else if (!isEmailValid(mail)) {
    showError(mail1, "Wrong Email-id");
  } else {
    showSuccess(mail1);
    valid = true;
  }
  return valid;
};

const checkpass = () => {
  let valid = false;

  const pass = pass1.value.trim();

  if (!isRequired(pass)) {
    showError(pass1, "Password cannot be blank.");
  } else {
    showSuccess(pass1);
    valid = true;
  }
  return valid;
};

const isEmailValid = (email) => {
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};


const isRequired = (value) => (value === "" ? false : true);
const isBetween = (length, min, max) =>
  length < min || length > max ? false : true;

const showError = (input, message) => {
  const formField = input.parentElement;

  formField.classList.remove("success");
  formField.classList.add("error");

  const error = formField.querySelector("small");
  error.textContent = message;
};

const showSuccess = (input) => {
  const formField = input.parentElement;

  formField.classList.remove("error");
  formField.classList.add("success");

  const error = formField.querySelector("small");
  error.textContent = "";
};

login.addEventListener("submit", function (e) {
  e.preventDefault();

  let ismailValid = checkmail(),
    ispassValid = checkpass();

  let isloginvalid = ismailValid && ispassValid;
  if (isloginvalid) {
  }
});

const debounce = (fn, delay = 500) => {
  let timeoutId;
  return (...args) => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      fn.apply(null, args);
    }, delay);
  };
};

login.addEventListener(
  "input",
  debounce(function (e) {
    switch (e.target.id) {
      case "mail":
        checkmail();
        break;
      case "pass":
        checkpass();
        break;
    }
  })
);