<script setup>
import { logoutUser, sameLoggedinUser } from '@/fns';
import { getAPI } from '@/httpreqs';
import { onMounted, ref } from 'vue';
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router';

const router = useRouter();
const route = useRoute();

const professionalID = route.params.id;

const professionalFound = ref(false);
const professional = ref({});

const message = ref('');


async function initialLoad() {
  const response = await getAPI({ url: '/api/professional', params: { 'id': professionalID } });
  if (response.data.found) {
    professionalFound.value = true;
    professional.value = response.data.professional;
  } else {
    message.value = 'Professional Not Found';
  }
  if (professional.value.approval === 'REJECTED') {
    router.push({ name: 'professional_suspension_notice' });
  }
  if (!sameLoggedinUser(professional.value.user.email)) {
    router.push({ name: 'professional_access_not_allowed' });
  }
}

async function onLogoutClick() {
  logoutUser();
  router.push({ name: 'login' });
}

onMounted(initialLoad);

</script>
<template>
    <div class="font-fira">
      <!-- Base structure: After Login -->
      <!-- Header / Logo / Site -->
      <nav class="navbar bg-primary">
        <div class="navbar-start">
          <a href="#" class="btn btn-lg btn-ghost text-2xl">
            Welcome, {{ professionalFound ? professional.user.fullname : 'Error' }} <span class="opacity-60">[PROFESSIONAL]</span>
          </a>
        </div>

        <div class="navbar-center">
          <ul class="menu menu-lg menu-horizontal">

            <li><RouterLink :to="{ name: 'professional_home', params: { id: professionalID } }" class="btn btn-ghost">Home</RouterLink></li>
            <li><RouterLink :to="{ name: 'professional_search' }" class="btn btn-ghost">Search</RouterLink></li>
          </ul>
        </div>
        <div class="navbar-end">
          <RouterLink :to="{ name: 'professional_profile_details', params: { id: professionalID } }" class="btn btn-ghost text-lg"> Profile </RouterLink>
          <button @click.prevent="onLogoutClick" class="btn btn-ghost text-lg"> Logout </button>
        </div>
      </nav>

      <div class="flex flex-col mt-8 mb-24 gap-8 items-center justify-center">
        <RouterView />
      </div>
    </div>
</template>
