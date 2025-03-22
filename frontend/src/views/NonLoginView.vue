<script setup>
import { logoutUser } from '@/fns';
import { useRouter } from 'vue-router';

const router = useRouter();

async function onLogoutClick() {
  logoutUser();
  router.push({ name: 'login' });
}

</script>
<template>
  <div class="font-fira">
    <!-- Base structure: After Login -->
    <!-- Header / Logo / Site -->
    <nav class="navbar bg-primary">
      <div class="navbar-start">
        <a href="#" class="btn btn-lg btn-ghost text-2xl">
          Welcome <span class="opacity-60">[USER]</span>
        </a>
      </div>

      <div class="navbar-center">
        <ul class="menu menu-lg menu-horizontal">
        </ul>
      </div>
      <div class="navbar-end">
        <button @click.prevent="onLogoutClick" class="btn btn-ghost text-lg"> Logout </button>
      </div>
    </nav>

    <div class="flex flex-col mt-8 mb-24 gap-8 items-center justify-center">
      <RouterView />
    </div>
  </div>
</template>
