const axios = require("axios");
jest.mock("axios");

const BaseUrl = "https://dev-5jcgg3zvw-dons-projects-72d00e99.vercel.app";

const mockregisterationdetails = {
  "status": "success",
  "message": "Registration Successful",
  "data": {
    'accessToken': "xxxxxxxxxxxx",
    "user": {
      userId: "67ggdnhvns",
      firstName: "osowo",
      lastName: "obi",
      email: "osoobi@gmail.com",
      phone: "09065453212",
      password: "12345"
    }
  }
};

const failedmockregistertiondetails = {
  "errors": [
    {
      "field": "string",
      "message": "string"
    },
  ]
};

const mocklogindetails = {
  "status": "success",
  "message": "Login Successful",
  "data": {
    'accessToken': "xxxxxxxxxxxx",
    "user": {
      userId: "567ggdnhvns",
      firstName: "osowo",
      lastName: "obi",
      email: "osoobi@gmail.com",
      phone: "09065453212",
      password: "12345"
    }
  }
};

const failedmocklogindetails = {
  "errors": [
    {
      "field": "string",
      "message": "string"
    },
  ]
};

const failedpassworddetails = {
  "status": "Bad request",
  "message": "Authentication failed",
  "statusCode": 401
};

const register = async (data) => {
  // Simulating successful Response
  axios.post.mockResolvedValueOnce({ data: mockregisterationdetails });
  const response = await axios.post(`${BaseUrl}/auth/register`, data);
  return response.data;
};

const registerwitherror = async (data) => {
  // Simulating error response
  axios.post.mockRejectedValueOnce({ response: { data: failedmockregistertiondetails } });
  try {
    await axios.post(`${BaseUrl}/auth/register`, data);
  } catch (error) {
    return error.response.data;
  }
};

const login = async (data) => {
  // Simulating successful response
  axios.post.mockResolvedValueOnce({ data: mocklogindetails });
  const response = await axios.post(`${BaseUrl}/auth/login`, data);
  return response.data;
};

const loginwithwrongpassword = async (data) => {
  axios.post.mockRejectedValueOnce({ response: { data: failedpassworddetails } });
  try {
    await axios.post(`${BaseUrl}/auth/login`, data);
  } catch (error) {
    return error.response.data;
  }
};

const loginwithmissingrequiredfield = async (data) => {
  axios.post.mockRejectedValueOnce({ response: { data: failedmocklogindetails } });
  try {
    await axios.post(`${BaseUrl}/auth/login`, data);
  } catch (error) {
    return error.response.data;
  }
};

describe('Registration Endpoint', () => {
  it('should successfully register a user', async () => {
    const user_data = { firstName: "osowo", lastName: "obi", email: "osoobi@gmail.com", phone: "09065453212", password: "12345" };
    const registereduser = await register(user_data);
    expect(registereduser).toEqual(mockregisterationdetails);
  });

  it('should handle validation errors such as repeated emails or userId or missing fields', async () => {
    const user_data = { email: "osoobi@gmail.com", phone: "09065453212" }; // missing some required fields e.g firstName, lastName
    const error = await registerwitherror(user_data);
    expect(error).toEqual(failedmockregistertiondetails);
  });
});

describe('Login Endpoint', () => {
  it('should successfully login a user', async () => {
    const user_data = { email: "osoobi@gmail.com", password: "12345" };
    const loggedinuser = await login(user_data);
    expect(loggedinuser).toEqual(mocklogindetails);
  });

  it('should return an unauthorized error', async () => {
    const user_data = { email: "osoobi@gmail.com", password: "wrongpassword" };
    const error = await loginwithwrongpassword(user_data);
    expect(error).toEqual(failedpassworddetails);
  });

  it('should return a validation error', async () => {
    const user_data = { email: "osoobi@gmail.com" };
    const error = await loginwithmissingrequiredfield(user_data);
    expect(error).toEqual(failedmocklogindetails);
  });
});
