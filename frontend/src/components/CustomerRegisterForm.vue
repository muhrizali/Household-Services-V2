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

let messages = ref([]);

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
      const resp = await postAPI({ url: "/api/customer", data: registerCustomerData() });
      if (resp.data.added) {
        addMessage("Successfully Registered");
        setTimeout(() => {
          router.push({ name: "login" });
        }, 2000)
      } else {
        addMessage("Error registering the user");
        addMessage(resp.data.message);
      }
    } else {
      addMessage("Invalid form inputs");
    }
  } catch (error) {
    addMessage("Error Registering the User");
  }
}

</script>
<template>
  <div class="card card-bordered w-1/2">
    <form @submit.prevent="onRegisterClick" class="card-body form-control">
      <h2 class="card-title text-2xl text-center">Customer Signup</h2>
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
              placeholder="JOHNDOE@ORG.COM"
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
              maxlength="200" 
              required 
              placeholder="JOHN DOE"
              class="input w-full input-bordered" />
              <!-- <p v-if="fullname.length > 5" class="text-error">Full name has too many characters</p> -->
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
              class="input w-full input-bordered" />
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
              placeholder="SECRET-PASSWORD"
              class="input w-full input-bordered" />
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
              placeholder="SECRET-PASSWORD"
              class="input w-full input-bordered" />
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
              placeholder="9876543210"
              class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="address">ADDRESS</label>
            </td>
            <td>
              <textarea 
              v-model="address_" 
              id="address" 
              required 
              name="address" 
              rows="4" 
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
              pattern="[0-9]{6}" 
              required 
              placeholder="123321"
              class="input w-full input-bordered" />
            </td>
          </tr>
        </tbody>
      </table>
      <input type="submit" value="REGISTERLOL" class="btn btn-block btn-lg btn-primary" />

      <p class="text-center pt-2">
        Already a member?
        <RouterLink to="/login" class="link link-primary">Login Here</RouterLink>
      </p>
    </form>
  </div>
</template>