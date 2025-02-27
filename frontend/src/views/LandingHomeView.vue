<script setup>
import { RouterLink, RouterView } from 'vue-router';
// import LoginForm from '@/components/LoginForm.vue';
</script>

<template>
  <div class="font-fira">
    <!-- LOGGED OUT BASE -->
    <nav class="navbar bg-primary">
      <div class="navbar-start">
        <a href="/" class="btn btn-lg btn-ghost text-xl">
          Household Services
        </a>
      </div>

      <div class="navbar-end">
        <div class="dropdown dropdown-end">
          <button tabindex="0" role="button" class="btn btn-ghost">
            Create Account
          </button>
          <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-md z-10 w-52 p-2 shadow">
            <li><RouterLink to="/register/customer">Customer Register</RouterLink></li>
            <li><RouterLink to="/register/professional">Professional Register</RouterLink></li>
          </ul>
        </div>

        <button class="btn btn-ghost">
          <RouterLink to="/login">Login</RouterLink>
        </button>

      </div>
    </nav>

    <div class="flex flex-col mt-8 mb-24 gap-8 items-center justify-center">
      <!-- Main Content -->
      <RouterView />
    </div>
  </div>

</template>
