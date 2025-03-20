<script setup>
import { getAPI, postAPI } from '@/httpreqs';
import router from '@/router';
import { computed, onMounted, ref } from 'vue';

let email_ = ref("");
let fullname_ = ref("");
let username_ = ref("");
let password_ = ref("");
let confirm_ = ref("");
let service_id_ = ref("")
let contact_ = ref("");
let experience_ = ref("");
let description_ = ref("");
let address_ = ref("");
let pincode_ = ref("");

let messages = ref([]);

let servicesData = ref([]);
// let errors = ref([]);

const registerProfessionalData = () => {
  return {
    "user": {
      "email": email_.value,
      "fullname": fullname_.value,
      "username": username_.value,
      "password": password_.value,
      "role": "PROFESSIONAL",
    },
    "professional": {
      "service_id": service_id_.value,
      "contact": contact_.value,
      "experience": experience_.value,
      "description": description_.value,
      "address": address_.value,
      "pincode": pincode_.value,
    }
  };
};

function addMessage(msg) {
  messages.value.push(msg);
}

function checkForm() {
  if (password_.value !== confirm_.value) {
    addMessage("Passwords do not match");
    return false;
  }
  return true;
}

async function onRegisterClick() {
  try {
    if (checkForm()) {
      const resp = await postAPI({ url: "/api/professional", data: registerProfessionalData() });
      if (resp.data.added) {
        addMessage("Successfully Registered User");
        setTimeout(() => {
          router.push({ name: "login" });
        }, 2000);
      } else {
        addMessage("Error Registering User");
        addMessage("Email, username or contact already exists");
      }
    } else {
      addMessage("Invalid form inputs");
    }
  } catch (error) {
    addMessage("Error Registering User");
  }
}  


onMounted(async function () {
  try {
    const resp = await getAPI({ url: "/api/service" });
    servicesData.value = resp.data.services;
  } catch (error) {
    servicesData.value = [ { id: 99, name: "Error Fetching Services" } ];
  }
})
</script>

<template>
  <div class="card card-bordered w-1/2">
    <form @submit.prevent="onRegisterClick" class="card-body form-control">
      <h2 class="card-title text-2xl text-center">Professional Signup</h2>
      <div v-if="messages.length"
        class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
        <ul>
          <li class="text-base-content" v-for="message in messages">{{ message }}</li>
        </ul>
      </div>
      <table class="table table-lg">
        <tbody>
          <tr>
            <td>
              <label for="email">EMAIL</label>
            </td>
            <td>
              <input 
              v-model="email_" 
              id="email" 
              type="email"
              required
              maxlength="200" 
              placeholder="EMAIL@ORG.COM" 
              class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="fullname">FULL NAME</label>
            </td>
            <td>
              <input 
              v-model="fullname_" 
              id="fullname" 
              type="text"
              required
              maxlength="200" 
              placeholder="JOHN DOE" 
              class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="username">USERNAME</label>
            </td>
            <td>
              <input 
              v-model="username_" 
              id="username" 
              type="text"
              required
              maxlength="30" 
              placeholder="JOHNDOE" 
              class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="password">PASSWORD</label>
            </td>
            <td>
              <input 
              v-model="password_" 
              id="password" 
              type="password"
              required
              maxlength="60"
              placeholder="SECRET"
              class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="confirm">CONFIRM PASSWORD</label>
            </td>
            <td>
              <input 
              v-model="confirm_" 
              id="confirm" 
              type="password"
              required
              maxlength="60" 
              placeholder="SECRET" 
              class="input w-full input-bordered">
            </td>
          </tr>

          <tr>
            <td>
              <label for="service_id">SERVICE</label>
            </td>
            <td>
              <select 
              v-model="service_id_" 
              name="service_id" 
              id="service_id"
              required 
              class="select w-full select-bordered">
                <option disabled value="" selected>--- SELECT ONE SERVICE ---</option>
                <option v-for="serviceData in servicesData" :value="serviceData.id">{{ serviceData.name || "Unknown" }}</option>
              </select>
            </td>
          </tr>

          <tr>
            <td>
              <label for="contact">CONTACT</label>
            </td>
            <td>
              <input 
              v-model="contact_" 
              id="contact" 
              type="tel"
              pattern="[0-9]{10}"
              required
              placeholder="PHONE NUMBER" 
              class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="experience">EXPERIENCE</label>
            </td>
            <td>
              <input 
              v-model="experience_" 
              id="experience" 
              type="number"
              required
              placeholder="YEARS" 
              class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="description">DESCRIPTION</label>
            </td>
            <td>
              <textarea 
              v-model="description_" 
              name="description" 
              id="description" 
              rows="4" 
              placeholder="ABOUT YOURSELF"
              class="textarea w-full textarea-bordered"></textarea>
            </td>
          </tr>
          <tr>
            <td>
              <label for="address">ADDRESS</label>
            </td>
            <td>
              <textarea 
              v-model="address_" 
              name="address" 
              id="address" 
              rows="4"
              required 
              placeholder="YOUR ADDRESS..."
              class="textarea w-full textarea-bordered"></textarea>
            </td>
          </tr>

          <tr>
            <td>
              <label for="pincode">PIN CODE</label>
            </td>
            <td>
              <input 
              v-model="pincode_" 
              id="pincode"
              type="text"
              required
              pattern="[0-9]{6}"
              placeholder="123321"
              class="input w-full input-bordered">
            </td>
          </tr>
        </tbody>
      </table>
      <input type="submit" value="REGISTER" class="btn btn-block btn-lg btn-primary" />

      <p class="text-center pt-2">
        Already a member?
        <RouterLink to="/login" class="link link-primary">Login here</RouterLink>
      </p>
    </form>
  </div>
</template>