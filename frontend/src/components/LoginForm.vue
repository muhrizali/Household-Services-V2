<script setup>
import { getAPI, postAPI } from '@/httpreqs';
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const email = ref("");
const password = ref("");

let message = ref("");
let loginData = computed(() => {
  return { "email": email.value, "password": password.value };
})

// authentication
// getAPI({ url: "/api/login" })
//   .then((resp) => test.value = resp.data)
//   .catch((err) => test.value = resp.data)

async function onLoginClick() {
  try {
    const resp = await postAPI({ url: "/api/login", data: loginData.value })
    if (resp.data.role === "CUSTOMER") {
      router.push({ name: "customer_home" });
    } else if (resp.data.role === "PROFESSIONAL") {
      router.push({ name: "professional_home" });
    } else if (resp.data.role === "ADMIN") {
      router.push({ name: "admin_home" })
    }
    message.value = "Logged In";
  } catch (error) {
    message.value = "Error Logging In";
  }
}


</script>
<template>
  <div class="card card-bordered w-1/2">
    <form @invalid="" class="card-body form-control">

      <h2 class="card-title text-2xl text-center">Login</h2>

      <!-- Login Form -->
      <table class="table table-lg">
        <tbody>
          <tr>
            <td>
              <label for="email">EMAIL</label>
            </td>
            <td>
              <input v-model="email" id="email" placeholder="EMAIL@ORG.COM" type="email" class="input w-full input-bordered" />
            </td>
          </tr>
          <tr>
            <td>
              <label for="password">PASSWORD</label>
            </td>
            <td>
              <input v-model="password" id="password" placeholder="YOUR-SECRET-PASSWORD" type="password" class="input w-full input-bordered" />
            </td>
          </tr>
        </tbody>
      </table>

      <button type="button" @click="onLoginClick" class="btn btn-block btn-lg btn-primary">LOGIN</button>
      <p class="text-center pt-2">
        New member?
        <RouterLink to="/register/customer" class="link link-primary">Create Account</RouterLink>
      </p>
    </form>
  </div>
</template>