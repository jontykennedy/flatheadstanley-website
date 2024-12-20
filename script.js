const subscribe = async (email, errorLabel, successLabel) => {
  try {
    const response = await fetch(`https://dn6jaadg7vtvplqlq32zlj7g4u0fvbhw.lambda-url.eu-west-2.on.aws/subscribe?email=${encodeURIComponent(email)}`);

    if (!response.ok) {
      if (response.status === 409) {
        successLabel.innerHTML = "You're already subscribed, check your emails for a verification link";
        return;
      }

      throw new Error();
    }

    successLabel.innerHTML = "Thanks, look out for a verification email";
  } catch (error) {
    errorLabel.innerHTML = "An error occurred, try again later";
  }
};

const submitNewsletterRequest = (e) => {
  const errorLabel = document.getElementById('email-error-label');
  const successLabel = document.getElementById('email-success-label');
  errorLabel.innerHTML = "";
  successLabel.innerHTML = "";

  const email = new FormData(e.target).entries().next().value[1];
  
  if (email.length === 0 || !email.includes("@")) {
    errorLabel.innerHTML = "Please enter a valid email!";
  } else {
    subscribe(email, errorLabel, successLabel);
  }

  const emailForm = document.getElementById('email');
  emailForm.value = "";

};