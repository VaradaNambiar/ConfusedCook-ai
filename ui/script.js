// DOM elements
const ingredientInput = document.getElementById("ingredientInput");
const cookButton = document.getElementById("cookButton");
const loadingIndicator = document.getElementById("loadingIndicator");
const resultsContainer = document.getElementById("resultsContainer");
const resultsContent = document.getElementById("resultsContent");
const errorContainer = document.getElementById("errorContainer");
const errorMessage = document.getElementById("errorMessage");

// Initialize
document.addEventListener("DOMContentLoaded", function () {
  // Cook button click
  cookButton.addEventListener("click", handleCookRequest);

  // Enter key press
  ingredientInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      handleCookRequest();
    }
  });
});

// Handle cook request
async function handleCookRequest() {
  response = await fetch("/health", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    console.log("error in health");
  }else{
    console.log(response.status)
  }
  const ingredients = ingredientInput.value.trim();

  if (!ingredients) {
    showError("Please enter some ingredients first!");
    return;
  }

  try {
    showLoading();
    hideError();
    hideResults();

    // mock API call
    const result = await mockAPICall(ingredients);
    hideLoading();
    showResults(result);
  } catch (error) {
    hideLoading();
    showError("Something went wrong. Please try again.");
  }
}

// Real API call to Flask backend
async function mockAPICall(ingredients) {
  try {
    const response = await fetch("/api/recipes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ingredients: ingredients }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status} \n err: ${response.body}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API call failed:", error);
    throw error;
  }
}

// Show/hide functions
function showLoading() {
  loadingIndicator.classList.remove("hidden");
  cookButton.disabled = true;
}

function hideLoading() {
  loadingIndicator.classList.add("hidden");
  cookButton.disabled = false;
}

function showResults(data) {
  const recipe = data.recipe;
  resultsContent.innerHTML = `
        <h2>${recipe.title}</h2>
        <p>${recipe.description}</p>
        
        <h3>Ingredients:</h3>
        <ul>
            ${recipe.ingredients
              .map((ingredient) => `<li>${ingredient}</li>`)
              .join("")}
        </ul>
        
        <h3>Instructions:</h3>
        <ol>
             ${recipe.instructions}
        </ol>
    `;
  resultsContainer.classList.remove("hidden");
}

function hideResults() {
  resultsContainer.classList.add("hidden");
}

function showError(message) {
  errorMessage.textContent = message;
  errorContainer.classList.remove("hidden");
}

function hideError() {
  errorContainer.classList.add("hidden");
}
