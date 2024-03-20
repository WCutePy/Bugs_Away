const uploadInput = document.getElementById('upload');
  // const filenameLabel = document.getElementById('filename');
  const imagePreview = document.getElementById('image-preview');
const form = document.getElementById('login-form');
  // Check if the event listener has been added before
  let isEventListenerAdded = false;
  uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];

    if (file) {
      // filenameLabel.textContent = file.name;

      const reader = new FileReader();
      reader.onload = (e) => {
        imagePreview.innerHTML =
          `<img src="${e.target.result}" class="max-h-48 rounded-lg mx-auto" alt="Image preview" />`;
        imagePreview.classList.remove('border-dashed', 'border-2', 'border-gray-400');

        // Add event listener for image preview only once
        if (!isEventListenerAdded) {
          imagePreview.addEventListener('click', () => {
            uploadInput.click();
          });

          isEventListenerAdded = true;
        }
      };
      reader.readAsDataURL(file);
    } else {
      filenameLabel.textContent = '';
      imagePreview.innerHTML =
        `<div class="bg-gray-200 h-48 rounded-lg flex items-center justify-center text-gray-500">No image preview</div>`;
      imagePreview.classList.add('border-dashed', 'border-2', 'border-gray-400');

      // Remove the event listener when there's no image
      imagePreview.removeEventListener('click', () => {
        uploadInput.click();
      });

      isEventListenerAdded = false;
    }
  });

  uploadInput.addEventListener('click', (event) => {
    event.stopPropagation();
  });





form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the file from the upload input
    const file = uploadInput.files[0];

    console.log("hi");

    if (file) {
        // Convert the file to a base64 string
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = async () => {
            // Append the base64 string as a hidden input to the form
            const base64Data = reader.result.split(',')[1];
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'image_data';
            hiddenInput.value = base64Data;
            form.appendChild(hiddenInput);

            // Submit the form
            form.submit();
        };
    }
});

  //
  // document.getElementById("proper-image-check").checked = false;