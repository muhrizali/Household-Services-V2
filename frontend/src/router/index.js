import { createRouter, createWebHistory } from 'vue-router';
import LoginForm from '@/components/LoginForm.vue';
import CustomerRegisterForm from '@/components/CustomerRegisterForm.vue';
import ProfessionalRegisterForm from '@/components/ProfessionalRegisterForm.vue';
import AdminHome from '@/components/admin/AdminHome.vue';
import Testing from '@/components/Testing.vue';
import DashboardView from '@/views/DashboardView.vue';
import LandingHomeView from '@/views/LandingHomeView.vue';
import CustomerHome from '@/components/customer/CustomerHome.vue';
import ProfessionalHome from '@/components/professionals/ProfessionalHome.vue';
import AdminServiceDetails from '@/components/admin/AdminServiceDetails.vue';
import AdminProfessionalDetails from '@/components/admin/AdminProfessionalDetails.vue';
import AdminCustomerDetails from '@/components/admin/AdminCustomerDetails.vue';
import AdminRequestDetails from '@/components/admin/AdminRequestDetails.vue';
import AdminServiceCreate from '@/components/admin/AdminServiceCreate.vue';
import AdminServiceDelete from '@/components/admin/AdminServiceDelete.vue';
import AdminServiceEdit from '@/components/admin/AdminServiceEdit.vue';
import AdminProfessionalApprove from '@/components/admin/AdminProfessionalApprove.vue';
import AdminProfessionalReject from '@/components/admin/AdminProfessionalReject.vue';
import AdminCustomerActivate from '@/components/admin/AdminCustomerActivate.vue';
import AdminCustomerBlock from '@/components/admin/AdminCustomerBlock.vue';
import AdminDashboardView from '@/views/AdminDashboardView.vue';
import AdminRequestEdit from '@/components/admin/AdminRequestEdit.vue';
import AdminRequestDelete from '@/components/admin/AdminRequestDelete.vue';
import AdminSearch from '@/components/admin/AdminSearch.vue';
// import HomeView from '../views/HomeView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: LandingHomeView,
      children: [
        {
          path: "",
          component: LoginForm
        },
        {
          path: "login",
          name: "login",
          component: LoginForm
        }
      ]
    },
    {
      path: '/register',
      component: LandingHomeView,
      children: [
        {
          path: "customer",
          name: "customer_register",
          component: CustomerRegisterForm
        },
        {
          path: "professional",
          name: "professional_register",
          component: ProfessionalRegisterForm
        }
      ]
    },
    {
      path: "/user",
      // component: DashboardView,
      children: [
        {
          path: "admin",
          component: AdminDashboardView,
          children: [
            {
              path: "",
              name: "admin_home",
              component: AdminHome
            },
            {
              path: "service/details/:id",
              name: "admin_service_details",
              component: AdminServiceDetails
            },
            {
              path: "service/create",
              name: "admin_service_create",
              component: AdminServiceCreate
            },
            {
              path: "service/delete/:id",
              name: "admin_service_delete",
              component: AdminServiceDelete
            },
            {
              path: "service/edit/:id",
              name: "admin_service_edit",
              component: AdminServiceEdit
            },
            {
              path: "professional/details/:id",
              name: "admin_professional_details",
              component: AdminProfessionalDetails
            },
            {
              path: "professional/approve/:id",
              name: "admin_professional_approve",
              component: AdminProfessionalApprove
            },
            {
              path: "professional/reject/:id",
              name: "admin_professional_reject",
              component: AdminProfessionalReject
            },
            {
              path: "customer/details/:id",
              name: "admin_customer_details",
              component: AdminCustomerDetails
            },
            {
              path: "customer/activate/:id",
              name: "admin_customer_activate",
              component: AdminCustomerActivate
            },
            {
              path: "customer/block/:id",
              name: "admin_customer_block",
              component: AdminCustomerBlock
            },
            {
              path: "request/details/:id",
              name: "admin_request_details",
              component: AdminRequestDetails
            },
            {
              path: "request/edit/:id",
              name: "admin_request_edit",
              component: AdminRequestEdit
            },
            {
              path: "request/delete/:id",
              name: "admin_request_delete",
              component: AdminRequestDelete
            },
            {
              path: "search/",
              name: "admin_search",
              component: AdminSearch
            },
          ]
        },
        {
          path: "customer",
          name: "customer_home",
          component: CustomerHome
        },
        {
          path: "professional",
          name: "professional_home",
          component: ProfessionalHome
        },
      ]
    },
    {
      path: "/testing",
      name: "testing",
      component: Testing
    }
  ],
});

export default router;
