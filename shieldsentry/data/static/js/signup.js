const name1 = document.querySelector("#name");
const mail1 = document.querySelector("#mail");
const passwordl = document.querySelector("#password1");
const password2 = document.querySelector("#password2");

const form = document.querySelector("#signup");

const checkUsername = () => {
  let valid = false;

  const min = 3,
    max = 25;

  const username = name1.value.trim();

  if (!isRequired(username)) {
    showError(name1, "Username cannot be blank");
  } else if (!isBetween(username.length, min, max)) {
    showError(name1, "Username not valid");
  } else {
    showSuccess(name1);
    valid = true;
  }
  return valid;
};

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

const checkPassword = () => {
  let valid = false;

  const password = passwordl.value.trim();

  if (!isRequired(password)) {
    showError(passwordl, "Password cannot be blank.");
  } else if (!isPasswordSecure(password)) {
    showError(
      passwordl,
      "Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)"
    );
  } else {
    showSuccess(passwordl);
    valid = true;
  }

  return valid;
};

const checkcPassword = () => {
  let valid = false;

  const cpassword1 = passwordl.value.trim();
  const cpassword2 = password2.value.trim();

  if (!isRequired(cpassword2)) {
    showError(password2, "Password cannot be blank.");
  } else if (!isPasswordSecure(cpassword2)) {
    showError(
      password2,
      "Password must has at least 8 characters that include at least 1 lowercase character, 1 uppercase characters, 1 number, and 1 special character in (!@#$%^&*)"
    );
  } else {
    if (cpassword1 == cpassword2) {
      showSuccess(password2);
      valid = true;
    } else {
      showError(password2, "password doesn't match");
    }
  }

  return valid;
};

const isEmailValid = (email) => {
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
};

const isPasswordSecure = (password) => {
  const re = new RegExp(
    "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})"
  );
  return re.test(password);
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

form.addEventListener("submit", function (e) {
  console.log();

  let isUsernameValid = checkUsername(),
    ismailValid = checkmail(),
    isPasswordValid = checkPassword(),
    iscPasswordValid = checkcPassword();

  let isFormValid =
    isUsernameValid && ismailValid && isPasswordValid && iscPasswordValid;

  if (isFormValid) {
    e.preventDefault();
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

form.addEventListener(
  "input",
  debounce(function (e) {
    switch (e.target.id) {
      case "name":
        checkUsername();
        break;
      case "mail":
        checkmail();
        break;
      case "password1":
        checkPassword();
        break;
      case "password2":
        checkcPassword();
        break;
    }
  })
);
