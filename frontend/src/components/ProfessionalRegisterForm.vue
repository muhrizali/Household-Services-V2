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

let message = ref("NOTHING");

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

onMounted(async function () {
  try {
    const resp = await getAPI({ url: "/api/service" });
    servicesData.value = resp.data.services;
  } catch (error) {
    servicesData.value = [ { id: 99, name: "Error Fetching Services" } ];
  }
})

async function onRegisterClick() {
  try {
    const resp = await postAPI({
      url: "/api/professional",
      data: registerProfessionalData()
    });
    message.value = "Successfully Registered User";
    router.push({ name: "login" });
  } catch (error) {
    message.value = "Error Registering User";
  }
}  
</script>

<template>
  <div class="card card-bordered w-1/2">
    <form method="post" class="card-body form-control">
      <h2 class="card-title text-2xl text-center">Professional Signup</h2>
      <table class="table table-lg">
        <tbody>
          <tr>
            <td>
              <label for="email">EMAIL</label>
            </td>
            <td>
              <input v-model="email_" id="email" type="email" placeholder="EMAIL@ORG.COM" class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="fullname">FULL NAME</label>
            </td>
            <td>
              <input v-model="fullname_" id="fullname" type="text" placeholder="JOHN DOE" class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="username">USERNAME</label>
            </td>
            <td>
              <input v-model="username_" id="username" type="text" placeholder="JOHNDOE" class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="password">PASSWORD</label>
            </td>
            <td>
              <input v-model="password_" id="password" type="password" placeholder="SECRET" class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="confirm">CONFIRM PASSWORD</label>
            </td>
            <td>
              <input v-model="confirm_" id="confirm" type="password" placeholder="SECRET" class="input w-full input-bordered">
            </td>
          </tr>

          <tr>
            <td>
              <label for="service_id">SERVICE</label>
            </td>
            <td>
              <select v-model="service_id_" name="service_id" id="service_id" class="select w-full select-bordered">
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
              <input v-model="contact_" id="contact" type="text" placeholder="PHONE NUMBER" class="input w-full input-bordered">
            </td>
          </tr>
          <tr>
            <td>
              <label for="experience">EXPERIENCE</label>
            </td>
            <td>
              <input v-model="experience_" id="experience" type="number" placeholder="YEARS" class="input w-full input-bordered">
            </td>
          </tr>
          <!-- <tr>
            <td>
              <label for="docs">DOCUMENTS</label>
            </td>
            <td>
              <input id="docs" type="file" class="file-input w-full file-input-bordered">
            </td>
          </tr> -->
          <tr>
            <td>
              <label for="description">DESCRIPTION</label>
            </td>
            <td>
              <textarea v-model="description_" name="description" id="description" rows="4" placeholder="ABOUT YOURSELF"
                class="textarea w-full textarea-bordered"></textarea>
            </td>
          </tr>
          <tr>
            <td>
              <label for="address">ADDRESS</label>
            </td>
            <td>
              <textarea v-model="address_" name="address" id="address" rows="4" placeholder="YOUR ADDRESS"
                class="textarea w-full textarea-bordered"></textarea>
            </td>
          </tr>

          <tr>
            <td>
              <label for="pincode">PIN CODE</label>
            </td>
            <td>
              <input v-model="pincode_" id="pincode" type="number" class="input w-full input-bordered">
            </td>
          </tr>
        </tbody>
      </table>
      <button type="button" @click="onRegisterClick" class="btn btn-block btn-lg btn-primary">REGISTER</button>

      <p class="text-center pt-2">
        Already a member?
        <RouterLink to="/login" class="link link-primary">Login here</RouterLink>
      </p>
    </form>
  </div>
</template>