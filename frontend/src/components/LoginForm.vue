<script setup>
import { getAPI, postAPI } from '@/httpreqs';
import { loginUser, checkAuth } from '@/fns';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const email = ref("");
const password = ref("");

const messages = ref([]);
const test = ref("s");

async function initialLoad() {
  const response = await checkAuth();
  if (response.logged_in) {
    addMessage("Login Successful");
    setTimeout(() => {
      if (response.role === "CUSTOMER") {
        router.push({ name: "customer_home", params: { id: response.id } });
      } else if (response.role === "PROFESSIONAL") {
        router.push({ name: "professional_home", params: { id: response.id } });
      } else if (response.role === "ADMIN") {
        router.push({ name: "admin_home" });
      }
    }, 0);
  } else {
    router.push({ name: 'login' });
  }
  test.value = response;
}

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
      const login = await loginUser(loginData());
      if (login.logged_in) {
        addMessage("Login Successful");
        setTimeout(() => {
          if (login.role === "CUSTOMER") {
            router.push({ name: "customer_home", params: { id: login.id } });
          } else if (login.role === "PROFESSIONAL") {
            router.push({ name: "professional_home", params: { id: login.id } });
          } else if (login.role === "ADMIN") {
            router.push({ name: "admin_home" });
          }
        }, 1000);
      }
    } else {
      addMessage("Check Your Email/Password");
    }
  } catch (error) {
    addMessage("Wrong Email/Password");
  }
}

onMounted(() => {
  initialLoad();
})

</script>
<template>
  <div class="card card-bordered w-1/2">
    <form class="card-body form-control">

      <h2 class="card-title text-2xl text-center">Login</h2>
      {{ test }}
      <div v-if="messages.length"
        class="bg-warning font-semibold p-4 my-4 rounded-md border-2 border-warning-content/50">
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
              <input v-model="password" id="password" placeholder="YOUR-SECRET-PASSWORD" type="password" required
                class="input w-full input-bordered" />
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