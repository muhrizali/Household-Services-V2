<script setup>
import { getAPI } from '@/httpreqs';
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

async function onLogoutClick() {
  const response = await getAPI({ url: "/api/login", params: { "logout": true } });
  if (response.data.logged_out) {
    router.push({ name: 'login' });
  }
}
</script>
<template>
    <div class="font-fira">
      <!-- Base structure: After Login -->
      <!-- Header / Logo / Site -->
      <nav class="navbar bg-primary">
        <div class="navbar-start">
          <RouterLink to="/testing" class="btn btn-lg btn-ghost text-2xl">
            Welcome, (Name) <span class="opacity-60">[CUSTOMER]</span>
          </RouterLink>
        </div>

        <div class="navbar-center">
          <ul class="menu menu-lg menu-horizontal">

            <li><RouterLink to="" class="btn btn-ghost">Home</RouterLink></li>
            <li><RouterLink to="" class="btn btn-ghost">Search</RouterLink></li>
          </ul>
        </div>
        <div class="navbar-end">
          <RouterLink class="btn btn-ghost text-lg"> Profile </RouterLink>
          <button @click.prevent="onLogoutClick" class="btn btn-ghost text-lg"> Logout </button>
        </div>
      </nav>

      <div class="flex flex-col mt-8 mb-24 gap-8 items-center justify-center">
        <RouterView />
      </div>
    </div>
</template>
