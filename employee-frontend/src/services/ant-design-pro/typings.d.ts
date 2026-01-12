declare namespace API {
  type CurrentUser = {
    id?: number;
    username?: string;
    employee_id?: string;
    email?: string;
    first_name?: string;
    last_name?: string;
    phone?: string;
    division?: number;
    division_name?: string;
    role?: string;
    type_of_employment?: string;
    status?: string;
    avatar?: string;
  };

  type LoginResult = {
    user?: CurrentUser;
    tokens?: {
      access: string;
      refresh: string;
    };
    message?: string;
  };

  type PageParams = {
    current?: number;
    pageSize?: number;
  };

  type RuleListItem = {
    key?: number;
    name?: string;
    desc?: string;
    callNo?: number;
    status?: number;
    updatedAt?: string;
    createdAt?: string;
    progress?: number;
  };

  type RuleList = {
    data?: RuleListItem[];
    total?: number;
    success?: boolean;
  };

  type LoginParams = {
    username?: string;
    password?: string;
    autoLogin?: boolean;
    type?: string;
  };
}
