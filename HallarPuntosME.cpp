#include <iostream>
#include <fstream>
#include <cassert>
#include <cmath>
#include <algorithm>
#include <cstdlib>
#include <ctime>

//Por favor compílelo así: g++ -o MinimaEntropia MinimaEntropia.cpp

void hallar_entropia(double tp_prueba, int dim_grilla[2], int N_datos, int n_as, double t_dat[], double u_dat[], double t0, double* dir);
void periodo_de_minima_entropia(double t_dat[], double u_dat[], double tp_menor, double tp_mayor, int grilla[2], int Finura, int N_fg, double max_Castigo[2], int N_filas, double t0, double *tablaPer, double *tabEnt);
int puntos_remanentes(int N_datos, double porcentaje_remover);
bool esta_el_numero(int elNumero, int elArray[], int N_revisar);
void remover_puntos(double tdat[], double udat[], int N_datos, int N_remanentes, double *t_nuevo, double *u_nuevo);
int minimos_puntos(double tp, double t[], double u[], int N_datos, double tp_menor, double tp_mayor, int dimGrilla[2], int Finura, int N_as, double t0, double porcentaje_inicial);

int main(int argc, char *argv[])
{
	/* :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	PARÁMETROS DE ENTRADA DEL PROGRAMA. 
	tp_menor=periodo menor de prueba en dias, tp_mayor=lo mismo pero el mayor, luego siguen las dimensiones de la grilla.
	La Finura es el número de periodos o frecuencias de prueba que se desea evaluar
	N_as es el exponente al cual se someten las funciones de castigo (ver void hallar_entropia)
	---------------------------------------------------------------------------------------------------------------------------------
	*/
	std::string nombre_archivo = argv[1];
	double tp_menor = atof(argv[2]);
	double tp_mayor = atof(argv[3]);
	int dimension1 = atoi(argv[4]);
	int dimension2 = atoi(argv[5]);
	int Finura = atoi(argv[6]);
	int N_as = atoi(argv[7]);
	double tp_estrella = atof(argv[8]);
	double porcentaje_ini = atof(argv[9]);
	int numCorridas = atoi(argv[10]);
	int dimGrilla[2] = {dimension1,dimension2};
	/*
	-----------------------------------------------------------------------------------------------------------------------------------
	FIN PARÁMETROS DE ENTRADA DEL PROGRAMA
	:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
	*/
	
	/* ################################################################################################################################
	LECTURA DEL ARCHIVO CON LOS DATOS
	En esta parte del código se asignan los datos de tiempo y de u a los arrays t[N_filas] y u[N_filas]
	En el primer ciclo for se lee el archivo para saber cuentos datos hay, es decir se halla N_filas
	En el segundo cilo se vuelve a leer el archivo para asignar cada dato en t[i] y u[i].
	----------------------------------------------------------------------------------------------------------------------------------
	*/
	std::ifstream read_file(nombre_archivo);
	assert(read_file.is_open());
	int N_filas=0;
	double tk, uk, delta_uk;
	while(!read_file.eof())
	{
		read_file >> tk >> uk >> delta_uk;
		N_filas++;
	}
	N_filas--;
	// Ahora que tenemos el número de filas podemos crear unos array que sabemos que tiene una longitud de N_filas
	// Las dos siguientes lineas es pa pedirle al read_file que vuelva a empezar desde el puro principio
	read_file.clear();
	read_file.seekg(std::ios::beg);
	double t[N_filas], u[N_filas];
	double delta_u; // esta linea porque read_file se confunde si no le aclaramos que son 3 columnas 
	
	assert(read_file.is_open());
	for (int i=0; i<N_filas; i++)
	{
		read_file >> t[i] >> u[i] >> delta_u;
		assert(read_file.good());
	}
	read_file.close();
	/*
	------------------------------------------------------------------------------------------------------------------------------------
	FIN DE LECTURA DE ARCHIVO CON LOS DATOS
	####################################################################################################################################
	*/
	double elPeriodo;
	double t0=t[0];
	int longitud_nombreAr=nombre_archivo.length();
	std::string nombre_nuevo="LosPuntosME_";
	for (int ji=0; ji<longitud_nombreAr-4; ji++){nombre_nuevo=nombre_nuevo+nombre_archivo[ji];}
	nombre_nuevo=nombre_nuevo+".csv";
	std::ofstream write_output(nombre_nuevo);
	assert(write_output.is_open());
	int N_minimo[numCorridas];
	for (int n=0; n<numCorridas; n++)
	{
		N_minimo[n]=minimos_puntos(tp_estrella,t,u,N_filas,tp_menor,tp_mayor,dimGrilla,Finura,N_as,t0,porcentaje_ini);
		std::cout << "Con " << N_minimo[n] << " puntos halló el periodo \n";
		if (n==numCorridas-1) {write_output << N_minimo[n] << "\n";}
		else {write_output << N_minimo[n] << ",";}
	}
	return 0;
}

int minimos_puntos(double tp, double t[], double u[], int N_datos, double tp_menor, double tp_mayor, int dimGrilla[2], int Finura, int N_as, double t0, double porcentaje_inicial)
{
	int N_ini=puntos_remanentes(N_datos, porcentaje_inicial);
	int N_min=N_ini-1;
	int maxBusq=N_datos-N_ini;
	int cBusq=0;
	bool encontro=false;
	double maxRest[2];
	while ((encontro==false)&&(cBusq<=maxBusq))
	{
		N_min++;
		double *t_nuevo = new double[N_min];
		double *u_nuevo = new double[N_min];
		double *periodos_dest = new double [10];
		double *ent_dest = new double [10];
		remover_puntos(t,u,N_datos,N_min,t_nuevo,u_nuevo);
		double *paramIni = new double[3];
		//NOTA: POR FAVOR NO BORRE ESTE std::cout. Por alguna locura, el programa deja de funcionar si lo borra.
		//C++ se pone emocional y se la pasa botando Segmentation Fault
		std::cout << "Evaluando el periodo en: " << N_min << " puntos. \n";
		//Gracias. :) :) ****************************************************************************************
		hallar_entropia(tp,dimGrilla,N_min,N_as,t_nuevo,u_nuevo,t0,paramIni);
		maxRest[0]=1.5*paramIni[1];
		maxRest[1]=1.5*paramIni[2];
		periodo_de_minima_entropia(t_nuevo,u_nuevo,tp_menor,tp_mayor,dimGrilla,Finura,N_as,maxRest,N_min,t0,periodos_dest,ent_dest);
		for (int i=0; i<10; i++)
		{
			if ((std::abs(periodos_dest[i]-tp)/tp)<=1e-4)
			{
				encontro=true;
			}
		}
		cBusq++;
		delete[] paramIni;
		delete[] t_nuevo;
		delete[] u_nuevo;
		delete[] periodos_dest;
		delete[] ent_dest;
	}
	return N_min;
}

/*
#####################################################################################################################################
:::::::FUNCIÓN QUE REMUEVE TODOS LOS PUNTOS EXCEPTO N_remanentes PUNTOS ALEATORIOS QUE SE QUEDAN:::::::::::::::::::::::::::::::::::::
#####################################################################################################################################
Esta función escoge una muestra de N_remanentes puntos de los N_datos totales en los arrays de tdat[] y udat[]. También deja de 
primero en el nuevo array el item con menor tiempo t. 
*/
void remover_puntos(double tdat[], double udat[], int N_datos, int N_remanentes, double *t_nuevo, double *u_nuevo)
{
	int escogidos[N_remanentes];
	int min_num=N_datos;
	int indiceMin;
	double t_min, u_min;
	srand(time(NULL));
	for (int j=0; j<N_remanentes; j++)
	{
		int numero_escogido=rand() % N_datos;
		if (j!=0)
		{
			while (esta_el_numero(numero_escogido, escogidos, j))
			{
				numero_escogido=rand() % N_datos;
			}
			escogidos[j]=numero_escogido;
		}
		else {escogidos[j]=numero_escogido;}
		if (escogidos[j]<=min_num)
		{
			min_num=escogidos[j];
			indiceMin=j;
			t_min=tdat[escogidos[j]];
			u_min=udat[escogidos[j]];
		}
		t_nuevo[j]=tdat[escogidos[j]];
		u_nuevo[j]=udat[escogidos[j]];
	}
	escogidos[indiceMin]=escogidos[0];
	t_nuevo[indiceMin]=t_nuevo[0];
	u_nuevo[indiceMin]=u_nuevo[0];
	escogidos[0]=min_num;
	t_nuevo[0]=t_min;
	u_nuevo[0]=u_min;
}
/*
#####################################################################################################################################
::::::::::::::::::::::::::::::::::::::::: FUNIÓN DE BÚSQUEDA DE UN int EN UN ARRAY ::::::::::::::::::::::::::::::::::::::::::::::::::
#####################################################################################################################################
Esta función busca si elNumero está dentro de elArray en los primeros N_revisar elementos de este 
*/
bool esta_el_numero(int elNumero, int elArray[], int N_revisar)
{
	bool encontro=false;
	for (int j=0; j<N_revisar; j++)
	{
		if (elNumero==elArray[j])
		{
			encontro=true;
		}
	}
	return encontro;
}

/*
#####################################################################################################################################
:::::::::::::::: FUNCIÓN QUE HAYA EL NÚMERO DE PUNTOS QUE QUEDAN AL REMOVER CIERTO PORCENTAJE DE PUNTOS :::::::::::::::::::::::::::::
#####################################################################################################################################
EL título dice lo siguiente, por ejemplo si le mete un puntos_remanentes(100,0.97) le devuelve 3.
*/
int puntos_remanentes(int N_datos, double porcentaje_remover)
{
	int puntos_rem=(int)floor((1.0-porcentaje_remover)*N_datos);
	return puntos_rem;
}

/*
######################################################################################################################################
::::::::::::::::::::::::::::::::: FUNCIÓN QUE HALLA EL PERIODO DE LA ESTRELLA DADOS UNOS DATOS ts Y us :::::::::::::::::::::::::::::::
######################################################################################################################################
Esta función evalua la entropía para distintos periodos de prueba. En total evalua Finura periodos, distribuidos uniformemente entre
frecuencias de 1/tp_mayor y 1/tp_menor. 
######################################################################################################################################
*/
void periodo_de_minima_entropia(double t_dat[], double u_dat[], double tp_menor, double tp_mayor, int grilla[2], int Finura, int N_fg, double max_Castigo[2], int N_filas, double t0, double *tablaPer, double *tabEnt)
{
	double f_menor, f_mayor, entropia_raw,frecuencia, g, f, maxG, maxF;
	double entropia[Finura+1], periodo[Finura+1];
	double *dirResp = new double[3];
	double entropia_menor[10];
	int indices[10];
	maxG=max_Castigo[0];
	maxF=max_Castigo[1];
	f_menor=1.0/tp_mayor;
	f_mayor=1.0/tp_menor;
	for (int ee=0; ee<10; ee++) {entropia_menor[ee]=1.0;}
	for (int k=0; k<=Finura; k++)
	{
		frecuencia=f_menor+((f_mayor-f_menor)/Finura)*k;
		periodo[k]=1.0/frecuencia;
		hallar_entropia(periodo[k],grilla,N_filas,N_fg,t_dat,u_dat,t0,dirResp);
		entropia_raw=dirResp[0];
		g=dirResp[1];
		f=dirResp[2];
		if ((g>maxG)||(f>maxF))
		{
			if (k==0){entropia[k]=0.95;}
			else{entropia[k]=entropia[0];}
		}
		else
		{
			entropia[k]=entropia_raw;
		}
		int l=0;
		bool termino=false;
		while ((l<10)&&(termino==false))
		{
			if (entropia[k]<entropia_menor[l])
			{
				if ((k-indices[l])<=3)
				{
					entropia_menor[l]=entropia[k];
					indices[l]=k;
					termino=true;
				}
				else
				{
					if (l<9) {entropia_menor[l+1]=entropia_menor[l]; indices[l+1]=indices[l];}
					entropia_menor[l]=entropia[k];
					indices[l]=k;
					termino=true;
				}
			}
			else
			{
				if ((k-indices[l])<=3) {termino=true;}
			}
			l=l+1;
		}
	}
	for (int n=0;n<10;n++)
	{
		tablaPer[n]=periodo[indices[n]];
		tabEnt[n]=entropia[indices[n]];
	}
}

/*
################################################################################################################################
:::::::::::::::::::::::::::::::::::::::::______¡¡¡¡¡ADVERTENCIA!!!!!!!_______:::::::::::::::::::::::::::::::::::::::::::::::::
###############################################################################################################################
Esta función evalua la entropía y los valores de f y g para cierto periodo de prueba
¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡ ¡¡¡¡    POR FAVOR NO LA TOQUE!!!!! YA SE COMPROBÓ QUE FUNCIONA MUY BIEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##############################################################################################################################
*/
void hallar_entropia(double tp_prueba, int dim_grilla[2], int N_datos, int n_as, double t_dat[], double u_dat[], double t0, double* dir)
{
	double phi[N_datos], xi[dim_grilla[0]];
	double inf_u, sup_u, paso_phi, paso_u, entropia, entropia_norm, xc, g, f, g_eval, f_eval, A, B, term_g, term_f;
	double *min_u, *max_u;
	int indice_i, indice_j;
	int cuenta_grilla[dim_grilla[0]][dim_grilla[1]];
	double grilla[dim_grilla[0]][dim_grilla[1]];
	for (int i=0; i<dim_grilla[0]; i++) { for (int j=0; j<dim_grilla[1]; j++) { cuenta_grilla[i][j]=0;}}
	// Aquí abajo vamos a hacer el equivalente de transformar_ts y clasificar los datos, de una, cada dato en cada una de las posiciones de la grilla
	// i es el índice que representa la cantidad de cuadros que tendrá el eje phi
	// j es el índice que represente la cantidad de cuadros que tendrá el eje u 
	// es decir dim_grilla debe colocarse así: {cuadros_phi, cuadros_u}
	A=dim_grilla[0];
	min_u=std::min_element(u_dat,u_dat+N_datos); //Esto devuelve el pointer donde está el mínimo de u
	max_u=std::max_element(u_dat,u_dat+N_datos); //Esto devuelve el pointer donde está el máximo de u
	paso_phi=1.0/dim_grilla[0]; // Ojo al operar 2 int si no ponemos 1.0 sino solo 1, c++ redondea al int mas pequeño. 
	paso_u=(*max_u-*min_u)/dim_grilla[1];
	for (int l=0; l<N_datos; l++)
	{
		phi[l]=((t_dat[l]-t0)/tp_prueba)-floor((t_dat[l]-t0)/tp_prueba);
		for (int i=0; i<dim_grilla[0]; i++)
		{
			if (phi[l]>=(i*paso_phi) && phi[l]<((i+1)*paso_phi))
			{
				indice_i=i;
			}
		}
		for (int j=0; j<dim_grilla[1]; j++)
		{
			if (u_dat[l]>=(*min_u+j*paso_u) && u_dat[l]<(*min_u+(j+1)*paso_u))
			{
				indice_j=j;
			}
		}
		cuenta_grilla[indice_i][indice_j]++;
	}
	//Ahora que tenemos la grilla en números enteros, vamos a hallar la entropía correspondiente a esa grilla
	entropia=0;
	g_eval=0;
	f_eval=0;
	for (int i=0; i<dim_grilla[0]; i++)
	{
		xi[i]=0;
		for (int j=0; j<dim_grilla[1]; j++)
		{
			if (cuenta_grilla[i][j]==0){}
			else
			{
				xc=(cuenta_grilla[i][j]+0.0)/N_datos;
				entropia=entropia+(-xc)*log(xc);
				xi[i]=xi[i]+xc;
				//Recuerda que si vas a operar dos int, tienes que agregar un +0.0 para que la respuesta te salga con decimales.
			}
		}
		term_f=pow(A, 0.5*n_as*A*A*(std::abs(xi[i]-(1.0/A))));
		if (i==0)
		{
			term_g=0.0;
		}
		else
		{
			term_g=pow(A, 0.5*n_as*A*A*(std::abs(xi[i]-xi[i-1])));
		}
		g_eval=g_eval+term_g;
		f_eval=f_eval+term_f;
	}
	f=(1/(A+1))*(log(f_eval)/log(A));
	g=(1/(A+(log(A-1)/log(A))))*(log(g_eval)/log(A));
	//std::cout<<"El valor de g es: "<<g<<" \n";
	entropia_norm=(1.0/log(dim_grilla[0]*dim_grilla[1]))*entropia;
	dir[0]=entropia_norm;
	dir[1]=g;
	dir[2]=f;
}
