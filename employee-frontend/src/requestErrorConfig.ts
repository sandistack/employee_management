import type { RequestOptions } from '@@/plugin-request/request';
import type { RequestConfig } from '@umijs/max';
import { message, notification } from 'antd';
import type { AxiosRequestConfig } from 'axios';

/**
 * @name 错误处理
 * pro 自带的错误处理， 可以在这里做自己的改动
 * @doc https://umijs.org/docs/max/request#配置
 */
export const errorConfig: RequestConfig = {
  // Base URL untuk Django backend
  baseURL: 'http://localhost:8000',

  errorConfig: {
    errorHandler: (error: any, opts: any) => {
      if (opts?.skipErrorHandler) throw error;

      if (error.response) {
        const status = error.response.status;
        const detail =
          error.response.data?.error || error.response.data?.detail || error.message;
        if (status === 401) {
          message.error('Sesi berakhir, silakan login ulang.');
        } else {
          notification.error({
            message: `Error ${status}`,
            description: detail || 'Terjadi kesalahan pada permintaan.',
          });
        }
      } else if (error.request) {
        message.error('Tidak ada respon dari server, coba lagi.');
      } else {
        message.error('Request error, silakan coba lagi.');
      }

      throw error;
    },
  },

  // Attach Authorization header when token exists
  requestInterceptors: [
    (config: RequestOptions) => {
      const accessToken = localStorage.getItem('accessToken');
      const headers: AxiosRequestConfig['headers'] = {
        ...config.headers,
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      };

      return {
        ...config,
        headers,
      } as RequestOptions;
    },
  ],
};
