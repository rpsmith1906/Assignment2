#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

int hash_function(const char* word);
bool isnumeric (const char* word);
int check_words(FILE* fp, hashmap_t hashtable[], char* misspelled[]);
bool load_dictionary(const char* dictionary_file, hashmap_t hashtable[]);
bool check_word(const char* word, hashmap_t hashtable[]);

bool isnumeric (const char* word)
{
     int i ;
     char c='\0' ;
     char number = 'u' ;

     i=0 ;
     while ( word[i] != '\0' )
     {
          c = word[i] ;
          if ( i==0 )
          {
               if  (( c != '+' ) && (c != '-'))
               {
                    if ( isdigit (c) ) { number = 'n' ; }
                    else { number = 'a' ; }
               }
          }
          else
          {
               if ( isdigit (c) ) 
               {
                    if (  number == 'u' ) { number = 'n' ; }
               }
               else
               {
                    switch ( number )
                    {
                         case 'u' :
                              number = 'a' ;
                              break ;

                         case 'n' :
                              switch ( c )
                              {
                                   case '.' :
                                        number = 'f' ;
                                        break ;

                                   case 'E' :
                                        number = 'e' ;
                                        break ;

                                   default :
                                        number = 'a' ;
                              }
                              break ;

                         case 'f' :
                              switch ( c )
                              {
                                   case 'E' :
                                        number - 'e' ;
                                        break ;

                                   default :
                                        number = 'a' ;
                              }
                     }
               }
          }

          if ( number == 'a' ) { break ; }
          else { i++ ; }

     }
   
     i = strlen ( word ) ;
     if ( ! isdigit( word[i-1] )) { number = 'a' ; }

     if ( number == 'a' ) { return ( false ) ; }
     else { return ( true ) ; }
}

bool check_word(const char* word, hashmap_t hashtable[])
{
     int hash,i ;
     node* node = NULL ;
     char lword[LENGTH + 1] ;

     for ( i=0; i<=LENGTH; i++ ) { lword[i] = '\0' ; }

     i=0 ;
     while (( word[i] != '\0' ) && ( i <= LENGTH ))
     {
          if ( isalpha( word[i] ) ) { lword[i] = tolower(word[i]) ; }
          lword[i] = tolower( word[i] ) ;
          i++ ;
     }

     if ( i <= LENGTH ) { lword[i] = '\0' ; }
     else { return ( false ) ; }

     hash = hash_function(lword) ;

     if (( hash > HASH_SIZE-1 ) || ( hash < 0 )) { return ( false ) ; }
     node = hashtable[hash] ;

     while ( node != NULL )
     {
          if ( strcmp(lword, node->word ) == 0 )
          {
               return ( true ) ;
          }

          node = node->next ;
     }
     return ( false ) ;
}

int check_words(FILE* fp, hashmap_t hashtable[], char* misspelled[])
{
     char word[LENGTH + 1] ;
     char lword[LENGTH + 1] = "" ;
     char c = '\0' ;
     int i = 0, j = 0 ;
     int mswords = 0 ;
     int punct = 0 ;

     for ( i=0 ; i<LENGTH ; i++ ) { word[i] = '\0' ; }
     while ( ! feof( fp ))
     {
          c = fgetc(fp) ;
          char *j ;
          i = 0 ;
          strcpy(word, "") ;

          if ( ispunct(c) ) { continue ; }

          while (( ! isspace(c) ) && ( c != '-' ))
          {
               if ( feof(fp) ) { break ; }
               if ( i <= LENGTH)
               {
                    word[i] = c ;
                    i++ ;
               }
               c = fgetc(fp) ;
          }

          if ( i <= LENGTH ) { word[i] = '\0' ; }
          else 
          { 
               word[LENGTH] = '\0' ;
               misspelled[mswords] = (char* )malloc(sizeof(char)*(LENGTH + 1)) ;
               if ( misspelled[mswords] == NULL ) 
               {
                    printf("System exceeded available memory..\n") ;
                    return (-1) ;
               }
               strcpy ( misspelled[mswords++], word ) ;
               word[0] = '\0' ;
          }

          while (( i > 1 ) && ( ispunct( word[i-1] )))
          {
               word[i-1] = '\0' ;
               i-- ;
          }

          if ( strlen(word) != 0 ) 
          { 
               if ( check_word(word, hashtable) == false ) 
               { 
                    j = strchr(word, '-') ;

                    if ( j != NULL ) 
                    {
                         j = strtok(word, "-" ) ;
                         if ( check_word(word, hashtable) == false )
                         {
                              misspelled[mswords] = (char* )malloc(sizeof(char)*(LENGTH + 1)) ;
                              if ( misspelled[mswords] == NULL ) 
                              {
                                   printf("System exceeded available memory..\n") ;
                                   return (-1) ;
                              }
                              strcpy ( misspelled[mswords++], word ) ;

                              j = strtok(NULL, "-") ;
                              while ( j != NULL )
                              {
                                   if ( check_word(word, hashtable) == false )
                                   {
                                        if ( misspelled[mswords] == NULL ) 
                                        {
                                             printf("System exceeded available memory..\n") ;
                                             return (-1) ;
                                        }
                                        misspelled[mswords] = (char* )malloc(sizeof(char)*(LENGTH + 1)) ;
                                        strcpy ( misspelled[mswords++], word ) ;
                                   }
                              }

                         }
                    } 
                    else
                    {
                         if ( ! isnumeric ( word ) )
                         {
                              misspelled[mswords] = (char* )malloc(sizeof(char)*(LENGTH + 1)) ;
                              if ( misspelled[mswords] == NULL ) 
                              {
                                   printf("System exceeded available memory..\n") ;
                                   return (-1) ;
                              }
                              strcpy ( misspelled[mswords++], word ) ;
                         }
                    }
               }
          }
     }

     return ( mswords ) ;
}

bool load_dictionary(const char* dictionary_file, hashmap_t hashtable[])
{
     char word[LENGTH + 1] ;
     int hash,i,len ;
     char c ;
     node* head ;
     FILE *fptr;

     for ( i=0 ; i<HASH_SIZE; i++ ) { hashtable[i] = NULL ; }

     if (( fptr = fopen(dictionary_file, "r")) == NULL )
     {
          printf ( "Error! could not open file %s\n", dictionary_file ) ;
          return ( false ) ;
     }

     c = fgetc(fptr) ;

     while ( ! feof(fptr) )
     {
          for ( i=0; i<=LENGTH; i++ ) { word[i] = '\0' ; }

          i = 0 ;
          while (( c != '\n' ) && ( c != '\r' ) && ( ! feof(fptr)))
          {
               if ( i <= LENGTH ) 
               { 
                    if ( isalpha(c) ) { word[i] = tolower(c) ; }
                    else { word[i] = c ; }
                    i++ ;
               }
               c = fgetc(fptr) ;
          }

          if ( i <= LENGTH ) { word[i] = '\0' ; }
          else { word[0] = '\0' ; }

          if ( strlen(word) != 0 ) 
          { 
               hash = hash_function(word) ;

               if ( hash < HASH_SIZE )
               {
                    head = hashtable[hash] ;

                    hashtable[hash] = (node*)malloc(sizeof(node)) ;

                    if ( hashtable[hash] == NULL )
                    {
                         printf( "Error creating a new node.\n" ) ;
                         return ( false ) ;
                    }
                    hashtable[hash]->next = head ;
                    strcpy ( hashtable[hash]->word, word ) ;
               }
          }
          c = fgetc(fptr) ;
     }

     fclose(fptr) ;
     return ( true ) ;
}
