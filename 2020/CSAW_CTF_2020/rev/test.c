int sub_402554(int x){
    return 0;
}

int sub_402637(int x){
    return 0;
}

int check_cheat_codes(){
	int x = 0;

	while (x <= 3){

		if (sub_402554(x) == 0)
			return 0;

	    if (sub_402637(x) != 0)
			x++;

        else
            return 0;

	}
	return 1;
}

int main(){
    return 0;
}
