/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2025 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
  'use strict'

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  const setTheme = theme => {
    if (theme === 'auto') {
      document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'))
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  setTheme(getPreferredTheme())

  const showActiveTheme = (theme, focus = false) => {
    const themeSwitcher = document.querySelector('#bd-theme')

    if (!themeSwitcher) {
      return
    }

    const themeSwitcherText = document.querySelector('#bd-theme-text')
    const activeThemeIcon = document.querySelector('.theme-icon-active use')
    const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
    const svgOfActiveBtn = btnToActive.querySelector('svg use').getAttribute('href')

    document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
      element.classList.remove('active')
      element.setAttribute('aria-pressed', 'false')
    })

    btnToActive.classList.add('active')
    btnToActive.setAttribute('aria-pressed', 'true')
    activeThemeIcon.setAttribute('href', svgOfActiveBtn)
    const themeSwitcherLabel = `${themeSwitcherText.textContent} (${btnToActive.dataset.bsThemeValue})`
    themeSwitcher.setAttribute('aria-label', themeSwitcherLabel)

    if (focus) {
      themeSwitcher.focus()
    }
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme())
    }
  })

  window.addEventListener('DOMContentLoaded', () => {
    showActiveTheme(getPreferredTheme())

    document.querySelectorAll('[data-bs-theme-value]')
      .forEach(toggle => {
        toggle.addEventListener('click', () => {
          const theme = toggle.getAttribute('data-bs-theme-value')
          setStoredTheme(theme)
          setTheme(theme)
          showActiveTheme(theme, true)
        })
      })
  })


  // Load states when country is selected
  // document.getElementById("country-select").addEventListener("change", function () {

  //   const countryName = this.value;
  //   const stateSelect = document.getElementById("state-select");

  //   stateSelect.innerHTML = "<option>Loading states...</option>";

  //   fetch("https://countriesnow.space/api/v0.1/countries/states", {

  //     method: "POST",

  //     headers: {
  //       "Content-Type": "application/json"
  //     },

  //     body: JSON.stringify({
  //       country: countryName
  //     })

  //   })
  //     .then(response => response.json())
  //     .then(data => {

  //       stateSelect.innerHTML = '<option value="">Select State</option>';

  //       if (data.data.states.length === 0) {

  //         stateSelect.innerHTML = '<option value="">No states available</option>';
  //         return;

  //       }

  //       data.data.states.forEach(state => {

  //         const option = document.createElement("option");

  //         option.value = state.name;
  //         option.textContent = state.name;

  //         stateSelect.appendChild(option);

  //       });

  //     });

  // });




  // COUNTRY
  document.addEventListener("DOMContentLoaded", function () {

    const countries = [
      "Nigeria",
      "United States",
      "United Kingdom",
      "Canada",
      "Ghana",
      "Germany",
      "France"
    ];

    const statesDB = {
      Nigeria: [
        "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa",
        "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo",
        "Ekiti", "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa",
        "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara",
        "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun",
        "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", "Zamfara"
      ],
      "United States": [
        "Alabama", "California", "Florida", "New York", "Texas"
      ]
    };

    // Populate all country selects
    document.querySelectorAll(".country-select").forEach(function (countrySelect) {

      const ticketId = countrySelect.dataset.ticketId;
      const stateSelect = document.getElementById("state-select" + ticketId);

      // Clear existing options
      countrySelect.innerHTML = "";

      // Default option
      const defaultOption = document.createElement("option");
      defaultOption.value = "";
      defaultOption.textContent = "Select Country";
      countrySelect.appendChild(defaultOption);

      // Populate countries
      const fragment = document.createDocumentFragment();
      countries.sort().forEach(function (country) {
        const option = document.createElement("option");
        option.value = country;
        option.textContent = country;
        fragment.appendChild(option);
      });
      countrySelect.appendChild(fragment);

      // Listen for country changes
      countrySelect.addEventListener("change", function () {

        const selectedCountry = this.value;
        stateSelect.innerHTML = '<option value="">Select State</option>';

        if (!statesDB[selectedCountry]) {
          stateSelect.innerHTML = '<option value="">No states available</option>';
          return;
        }

        const fragmentStates = document.createDocumentFragment();
        statesDB[selectedCountry].forEach(function (state) {
          const option = document.createElement("option");
          option.value = state;
          option.textContent = state;
          fragmentStates.appendChild(option);
        });

        stateSelect.appendChild(fragmentStates);

      });

    });

  });


  // Load states when country is selected
  // document.getElementById("country-select").addEventListener("change", function () {

  //   const countryName = this.value;
  //   const stateSelect = document.getElementById("state-select");

  //   stateSelect.innerHTML = "<option>Loading states...</option>";

  //   fetch("https://countriesnow.space/api/v0.1/countries/states", {

  //     method: "POST",

  //     headers: {
  //       "Content-Type": "application/json"
  //     },

  //     body: JSON.stringify({
  //       country: countryName
  //     })

  //   })
  //     .then(response => response.json())
  //     .then(data => {

  //       stateSelect.innerHTML = '<option value="">Select State</option>';

  //       if (data.data.states.length === 0) {

  //         stateSelect.innerHTML = '<option value="">No states available</option>';
  //         return;

  //       }

  //       data.data.states.forEach(state => {

  //         const option = document.createElement("option");

  //         option.value = state.name;
  //         option.textContent = state.name;

  //         stateSelect.appendChild(option);

  //       });

  //     });

  // });


  // Currency selection and fetching account details
  document.getElementById("currency-select").addEventListener("change", function () {

    const currency = this.value;
    const accountDiv = document.getElementById("account-details");

    if (currency === "") {

      accountDiv.style.display = "none";

      document.getElementById("currency-display").value = "";
      document.getElementById("account-number").value = "";
      document.getElementById("bank-name").value = "";
      document.getElementById("account-name").value = "";

      return;
    }

    // Show currency immediately
    document.getElementById("currency-display").value = currency;

    accountDiv.style.display = "block";

    fetch(`/get-account-details/?currency=${currency}`)
      .then(response => response.json())
      .then(data => {

        document.getElementById("account-number").value = data.account_number;
        document.getElementById("bank-name").value = data.bank_name;
        document.getElementById("account-name").value = data.account_name;

      });

  });

  document.addEventListener("DOMContentLoaded", function () {
    const exchangeRates = {
      "NGN": 1,
      "USD": 282.09,
      "GBP": 0.00051
    };

    document.querySelectorAll(".currency-select").forEach(select => {
      select.addEventListener("change", function () {
        const ticketId = this.dataset.ticketId;
        const priceElem = document.getElementById(`ticket-price${ticketId}`);
        const originalPrice = Number(this.dataset.originalPrice); // store in data-original-price
        const currency = this.value;

        if (!exchangeRates[currency]) return;

        const converted = (originalPrice * exchangeRates[currency]).toFixed(2);

        let symbol = currency === "NGN" ? "₦" : currency === "USD" ? "$" : "£";
        priceElem.textContent = `${symbol}${Number(converted).toLocaleString()}`;
      });
    });
  });

})()


