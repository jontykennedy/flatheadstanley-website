const unsubscribe = async (email, errorLabel, successLabel) => {
  try {
    const response = await fetch(`https://dn6jaadg7vtvplqlq32zlj7g4u0fvbhw.lambda-url.eu-west-2.on.aws/unsubscribe?email=${encodeURIComponent(email)}`);

    if (!response.ok) {
      throw new Error();
    }

    successLabel.innerHTML = "Unsubscribed successfully";
  } catch (error) {
    errorLabel.innerHTML = "An error occurred, try again later";
  }
};

const submitUnsubscribeRequest = (e) => {
  const errorLabel = document.getElementById('email-error-label');
  const successLabel = document.getElementById('email-success-label');
  errorLabel.innerHTML = "";
  successLabel.innerHTML = "";

  const email = new FormData(e.target).entries().next().value[1];
  
  if (email.length === 0 || !email.includes("@")) {
    errorLabel.innerHTML = "Please enter a valid email!";
  } else {
    unsubscribe(email, errorLabel, successLabel);
  }

  const emailForm = document.getElementById('email');
  emailForm.value = "";

  return;
};

