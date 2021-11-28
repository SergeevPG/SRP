import random
import string
import hashlib
from math import gcd


def generator_prime_numbers():
    n = 20000
    arr_nums = []
    for i in range(n + 1):
        arr_nums.append(i)
    arr_nums[1] = 0
    i = 2
    while i ** 2 <= n:
        if arr_nums[i] != 0:
            j = i ** 2
            while j < n:
                arr_nums[j] = 0
                j += i
        i += 1
    arr_nums = set(arr_nums)
    arr_nums.remove(0)
    arr_nums = list(arr_nums)
    arr_nums.sort()
    print(f"Массив простых чисел: {arr_nums}\nДлина массива: {len(arr_nums)}")
    q_index = random.randint(666, 1001)
    q = arr_nums[q_index]
    while True:
        N = 2 * q + 1
        # print(f"q = {q} \tN = {N}")
        if N not in arr_nums:
            q_index = random.randint(666, 1001)
            q = arr_nums[q_index]
            continue
        else:
            break
    return q, N


def generator_mod(N_input):
    # генератор по модулю N
    initial_set = set()
    current_set = set()
    for num in range(1, N_input):
        if gcd(num, N_input) == 1:
            initial_set.add(num)
    for g in range(1, N_input):
        for powers in range(1, N_input):
            current_set.add(pow(g, powers) % N_input)
        if initial_set == current_set:
            return g


def generator_salt():
    salt = ""
    for i in range(16):
        salt += random.choice(string.ascii_lowercase)
    return salt


q, N = generator_prime_numbers()
g = generator_mod(N)
k = 3
print(f"k = {k} (для простоты и производительности примем его за константу)")
print(f"q - простое число = {q}")
print(f"N - простое число = 2*q+1 = {N}")
print(f"g - генератор по mod N = {g}")


class Client():
    def __init__(self):
        self.login = "username"
        print(f"\nlogin = {self.login}")
        self.password = "passwordkey"
        print(f"password = {self.password}")
        self.salt = generator_salt()
        print(f"salt = {self.salt}")
        self.x = int(hashlib.sha512(self.salt.encode() + self.password.encode()).hexdigest(), 16)
        print(f"x - sha512(salt, password) = {self.x}")
        self.v = pow(g, self.x, N)
        print(f"v = g^x mod N = {self.v}")
        # для аутентификации
        self.a = 0
        self.A = 0
        self.B = 0
        self.u = 0
        # для общего ключа
        self.S = 0
        self.K = 0
        self.H_n = 0
        self.H_g = 0
        self.Hn_XOR_Hg = 0
        self.H_I = 0
        self.M_Client = 0
        self.R_Server = 0
        self.R_Client = 0

    def registration(self):
        server.login = self.login
        server.salt = self.salt
        server.v = self.v

    def Client_Authentication1(self):
        self.a = random.randint(100, 1000)
        print(f'\na (клиента) - случайное число = {self.a}')
        self.A = pow(g, self.a, N)
        print(f"A (клиента) = g^a mod N = {self.A}")
        server.A = self.A
        server.login = self.login

    def Client_Authentication2(self):
        if self.B != 0:
            self.u = int(hashlib.sha512(str(self.A).encode() + str(self.B).encode()).hexdigest(), 16)
            print(f"u (клиента) = sha512(A, B) = {self.u}")
            if self.u == 0:
                print("ОШИБКА!\nu не должен быть равен 0 !!!")
                return False
            else:
                return True
        else:
            print("ОШИБКА!\nB не должен быть равен 0 !!!")
            return False

    def Client_Generator_Key(self):
        self.S = pow((self.B - k * pow(g, self.x, N)), (self.a + self.u * self.x), N)
        print(f"\nS (клиента) = ( ( B - k * (g^x mod N) ) ^ (a + u * x) ) mod N = {self.S}")
        self.K = int(hashlib.sha512(str(self.S).encode()).hexdigest(), 16)
        print(f"K (клиента) = sha512(S) = {self.S}")

        self.H_n = int(hashlib.sha512(str(N).encode()).hexdigest(), 16)
        self.H_g = int(hashlib.sha512(str(g).encode()).hexdigest(), 16)
        self.Hn_XOR_Hg = self.H_n ^ self.H_g
        self.H_I = int(hashlib.sha512(str(self.login).encode()).hexdigest(), 16)
        self.M_Client = int(hashlib.sha512(str(self.Hn_XOR_Hg).encode() + str(self.H_I).encode() + str(self.S).encode() + str(self.A).encode() + str(self.B).encode() + str(k).encode()).hexdigest(), 16)
        print(f"M (клиента) = H( H(N) xor H(g), H(I), S, A, B, k ) = {self.M_Client}")
        server.M_Client = self.M_Client

    def Client_Generator_R(self):
        self.R_Client = int(hashlib.sha512(str(self.A).encode() + str(self.M_Client).encode() + str(self.K).encode()).hexdigest(),16)
        print(f"R (клиента) = H (A, M(клиента), K(клиента)) = {self.R_Client}")
        if self.R_Client == self.R_Server:
            print("\n\n\tВСЕ НАСТРОЕНО ВЕРНО !!!")
            return True
        else:
            return False


class Server():
    def __init__(self):
        self.login = ""
        self.salt = ""
        self.v = 0
        self.A = 0
        # для аутентификации
        self.b = 0
        self.B = 0
        self.u = 0
        # для общего ключа
        self.S = 0
        self.K = 0
        self.H_n = 0
        self.H_g = 0
        self.Hn_XOR_Hg = 0
        self.H_I = 0
        self.M_Server = 0
        self.M_Client = 0
        self.R_Server = 0

    def Server_Authentication1(self):
        if self.A != 0:
            self.b = random.randint(100, 1000)
            print(f'\nb (сервера) - случайное число = {self.b}')
            self.B = (k * self.v + pow(g, self.b, N)) % N
            print(f'B (сервера)= (k*v + g^b mod N) mod N = {self.B}')
            user.B = self.B

            self.u = int(hashlib.sha512(str(self.A).encode() + str(self.B).encode()).hexdigest(), 16)
            print(f"\nu (ceрвера) = sha512(A, B) = {self.u}")
            if self.u == 0:
                print("ОШИБКА!\nu не должен быть равен 0 !!!")
                return False
            else:
                return True
        else:
            print("ОШИБКА!\nA не должен быть равен 0 !!!")
            return False

    def Server_Generator_Key(self):
        self.S = pow(self.A * pow(self.v, self.u, N), self.b, N)
        print(f"\nS (сервера) = ( (A * (v^u mod N)) ^ b ) % N = {self.S}")
        self.K = int(hashlib.sha512(str(self.S).encode()).hexdigest(), 16)
        print(f"K (сервера) = sha512(S) = {self.S}")

        self.H_n = int(hashlib.sha512(str(N).encode()).hexdigest(), 16)
        self.H_g = int(hashlib.sha512(str(g).encode()).hexdigest(), 16)
        self.Hn_XOR_Hg = self.H_n ^ self.H_g
        self.H_I = int(hashlib.sha512(str(self.login).encode()).hexdigest(), 16)
        self.M_Server = int(hashlib.sha512(str(self.Hn_XOR_Hg).encode() + str(self.H_I).encode() + str(self.S).encode() + str(self.A).encode() + str(self.B).encode() + str(k).encode()).hexdigest(), 16)
        print(f"M (сервера) = H( H(N) xor H(g), H(I), S, A, B, k ) = {self.M_Server}")
        if self.M_Server == self.M_Client:
            self.R_Server = int(hashlib.sha512(str(self.A).encode() + str(self.M_Server).encode() + str(self.K).encode()).hexdigest(), 16)
            print(f"\nR (сервера) = H (A, M(сервера), K(сервера)) = {self.R_Server}")
            user.R_Server = self.R_Server
            return True
        else:
            print("ОШИБКА!\nM клиента не равна М сервера !!!")
            return False


if __name__ == '__main__':
    user = Client()
    server = Server()
    user.registration()
    user.Client_Authentication1()
    if server.Server_Authentication1():
        if user.Client_Authentication2():
            user.Client_Generator_Key()
            if server.Server_Generator_Key():
                if user.Client_Generator_R():
                    print("\nR клиента равна R сервера")
                else:
                    print("FATAL ERROR")
            else:
                print("FATAL ERROR")
        else:
            print("FATAL ERROR")
    else:
        print("FATAL ERROR")
