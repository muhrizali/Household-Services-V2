<script setup>
import { RouterLink, RouterView } from 'vue-router';

</script>
<template>
    <div class="font-fira">
      <!-- Base structure: After Login -->
      <!-- Header / Logo / Site -->
      <nav class="navbar bg-primary">
        <div class="navbar-start">
          <RouterLink to="/testing" class="btn btn-lg btn-ghost text-2xl">
            Welcome, Customer <span class="opacity-60">[CUSTOMER]</span>
          </RouterLink>
        </div>

        <div class="navbar-center">
          <ul class="menu menu-lg menu-horizontal">

            <li><RouterLink :to="{ name: 'admin_home' }" class="btn btn-ghost">Home</RouterLink></li>
            <li><RouterLink to="" class="btn btn-ghost">Search</RouterLink></li>
          </ul>
        </div>
        <div class="navbar-end">
          <!-- <RouterLink class="btn btn-ghost text-lg"> Profile </RouterLink> -->
          <RouterLink :to="{ name: 'login' }" class="btn btn-ghost text-lg"> Logout </RouterLink>
        </div>
      </nav>

      <div class="flex flex-col mt-8 mb-24 gap-8 items-center justify-center">
        <RouterView />
      </div>
    </div>
</template>
