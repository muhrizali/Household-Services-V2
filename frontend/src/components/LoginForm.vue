<script setup>
import { getAPI, postAPI } from '@/httpreqs';
import { ref, useTemplateRef } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const email = ref("");
const password = ref("");

const messages = ref([]);

function loginData() {
  return { "email": email.value, "password": password.value };
}

function addMessage(msg) {
  messages.value.push(msg);
}

function checkLoginForm() {

  let validEmail = (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value));
  let validPassword = (password.value.length > 0);

  if (!validEmail) {
    addMessage("EMAIL: Please enter valid email address");
  }
  if (!validPassword) {
    addMessage("PASSWORD: Please enter valid password");
  }

  return validEmail && validPassword;
}

async function onLoginClick() {
  try {
    messages.value = [];
    if (checkLoginForm()) {
      const resp = await postAPI({ url: "/api/login", data: loginData() });
      addMessage("Successfully logged in; Redirecting to dashboard");
      setTimeout(() => {
        if (resp.data.role === "CUSTOMER") {
          router.push({ name: "customer_home", params: { id: resp.data.id } });
        } else if (resp.data.role === "PROFESSIONAL") {
          router.push({ name: "professional_home" });
        } else if (resp.data.role === "ADMIN") {
          router.push({ name: "admin_home" });
        }
      }, 2000);
    } else {
      addMessage("Could Not Log You In");
    }
  } catch (error) {
    addMessage("Wrong Email or Password");
  }
}


</script>
<template>
  <div class="card card-bordered w-1/2">
    <form class="card-body form-control">

      <h2 class="card-title text-2xl text-center">Login</h2>
      <div v-if="messages.length" class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
        <ul>
          <li class="text-base-content" v-for="message in messages">{{ message }}</li>
        </ul>
      </div>

      <!-- Login Form -->
      <table class="table table-lg">
        <tbody>
          <tr>
            <td>
              <label for="email">EMAIL</label>
            </td>
            <td>
              <input v-model="email" id="email" placeholder="EMAIL@ORG.COM" type="email" required
                class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="password">PASSWORD</label>
            </td>
            <td>
              <input v-model="password" id="password" placeholder="YOUR-SECRET-PASSWORD" type="password"
                required class="input w-full input-bordered" />
            </td>
          </tr>
        </tbody>
      </table>

      <button type="button" @click="onLoginClick" class="btn btn-block btn-lg btn-primary">LOGIN</button>
      <p class="text-center pt-2">
        New member? <RouterLink :to="{ name: 'customer_register' }" class="link link-primary">Create Account
        </RouterLink>
      </p>
    </form>
  </div>
</template>