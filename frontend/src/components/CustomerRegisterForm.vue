<script setup>
import { getAPI, postAPI } from '@/httpreqs';
import router from '@/router';
import { computed, ref } from 'vue';

let email_ = ref("");
let fullname_ = ref("");
let username_ = ref("");
let password_ = ref("");
let confirm_ = ref("");
let contact_ = ref("");
let address_ = ref("");
let pincode_ = ref("");

let message = ref("");
let backResp = ref({});

// let errors = ref([]);

const registerCustomerData = () => {
  return {
    "user": {
      "email": email_.value,
      "fullname": fullname_.value,
      "username": username_.value,
      "password": password_.value,
      "role": "CUSTOMER"
    },
    "customer": {
      "contact": contact_.value,
      "address": address_.value,
      "pincode": pincode_.value
    }
  };
};

async function onRegisterClick() {
  try {
    const resp = await postAPI({ url: "/api/customer", data: registerCustomerData() });
    message.value = "Successfully Registered";
    router.push({ name: "login" });
  } catch(error) {
    message.value = "Error Registering the User";
  }
}

</script>
<template>
  <div class="card card-bordered w-1/2">
    <form method="post" class="card-body form-control">
      <h2 class="card-title text-2xl text-center">Customer Signup</h2>
      <p class="bg-warning">{{ message }}</p>
      <table class="table table-lg">
        <tbody>
          <tr>
            <td>
              <label for="email">EMAIL</label>
            </td>
            <td>
              <input v-model="email_" id="email" type="email" placeholder="JOHNDOE@ORG.COM"
                class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="fullname">FULL NAME</label>
            </td>
            <td>
              <input v-model="fullname_" id="fullname" type="text" placeholder="JOHN DOE"
                class="input w-full input-bordered" />
              <!-- <p v-if="fullname.length > 5" class="text-error">Full name has too many characters</p> -->
            </td>
          </tr>
          <tr>
            <td>
              <label for="username">USERNAME</label>
            </td>
            <td>
              <input v-model="username_" id="username" type="text" placeholder="JOHNDOE"
                class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="password">PASSWORD</label>
            </td>
            <td>
              <input v-model="password_" id="password" type="password" placeholder="SECRET-PASSWORD"
                class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="confirm">CONFIRM PASSWORD</label>
            </td>
            <td>
              <input v-model="confirm_" id="confirm" type="password" placeholder="SECRET-PASSWORD"
                class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="contact">CONTACT</label>
            </td>
            <td>
              <input v-model="contact_" id="contact" type="text" placeholder="PHONE NUMBER"
                class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="address">ADDRESS</label>
            </td>
            <td>
              <textarea v-model="address_" id="address" name="address" rows="4" placeholder="YOUR ADDRESS"
                class="textarea w-full textarea-bordered"></textarea>
            </td>
          </tr>
          <tr>
            <td>
              <label for="pincode">PIN CODE</label>
            </td>
            <td>
              <input v-model="pincode_" id="pincode" type="number" placeholder="PINCODE"
                class="input w-full input-bordered" />
            </td>
          </tr>
        </tbody>
      </table>
      <button type="button" @click.prevent="onRegisterClick" class="btn btn-block btn-lg btn-primary">REGISTER</button>

      <p class="text-center pt-2">
        Already a member?
        <RouterLink to="/login" class="link link-primary">Login Here</RouterLink>
      </p>
    </form>
  </div>
</template>